#!/usr/bin/env python3
"""Annotate a text file with the ExpoPortal (OntoPortal) Annotator and write a CSV\nwith one row per ontology term and the number of times it appears in the text.

Usage:
  EXPOPORTAL_APIKEY=... python3 annotate_file.py input.txt [-o out.csv] [--ontologies A,B] [--all-matches]
"""
import argparse, csv, json, os, re, sys, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor

API = "https://data.expoportal.biohackeu.bigcat-bioinformatics.org/annotator"

def annotate(text, apikey, ontologies=None, longest_only=True):
    params = {
        "text": text,
        "longest_only": str(longest_only).lower(),
        "exclude_numbers": "true",
        "whole_word_only": "true",
        "exclude_synonyms": "false",
        "display_context": "false",
    }
    if ontologies:
        params["ontologies"] = ontologies
    req = urllib.request.Request(
        API, data=urllib.parse.urlencode(params).encode(), method="POST",
        headers={"Authorization": f"apikey token={apikey}", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)

# Everyday / conversational words that match ontology terms but carry no meaning here.
STOPWORDS = set("""
a about above after again against all also am an and any are as at be because been before being below between both
but by can could did do does doing down during each few for from further had has have having he her here hers him his
how i if in into is it its just me more most my no nor not now of off on once only or other our out over own same she
should so some such than that the their them then there these they this those through to too under until up very was
we were what when where which while who whom why will with would you your
yes yeah yep no nope okay ok alright right mhm mm um er erm uh ah oh well like really actually sort kind
bit lot lots thing things stuff way ways time times day days today week year years good great fine nice lovely
sure mean means meant say said saying tell told know knew think thought go going gone went get got getting make made
take taking took come came see saw look looking want wanted need needed use used try tried put keep kept let
little big small long short high low early late new old first last next end start beginning part point case side
place set base level type form group class section open close clear free full whole real able able
one two three four five six seven eight nine ten hundred thousand
positive negative normal present absent same different
important difficult best better worse value source work works working read reading text sound affected
change changes changed difference person people field system kind question answer reason result
fact course anyway probably maybe perhaps quite pretty enough certain certainly obviously exactly
interviewer respondent int res
""".split())

# ---------------------------------------------------------------- demographics
SEX_PROP, MIN_AGE_PROP, MAX_AGE_PROP, RESIDENCE_PROP = "NCIT_C28421", "NCIT_C200031", "NCIT_C200032", "NCIT_C25273"
SEX_VALUES = {"female": ("NCIT_C16576", "Female"), "male": ("NCIT_C20197", "Male")}
def split_header(text):
    """Return (header, body). The header is everything before '[Start of recording]'
    or the first speaker tag."""
    m = re.search(r"(?m)^[ \t]*(?:\[(?i:start of recording)\]|[A-Z]{2,5}:)", text)
    if not m:
        return "", text
    # blank the header in the body so character offsets stay the same
    head = text[:m.start()]
    return head, "".join(c if c in "\r\n" else " " for c in head) + text[m.start():]

def header_fields(header):
    fields = {}
    for line in header.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            if v.strip():
                fields[k.strip().lower()] = v.strip()
    return fields

def demographics(header, participant, apikey):
    f = header_fields(header)
    rows = []
    def add(prop, plabel, value, vlabel="", note=""):
        rows.append({"participant": participant, "property": "obo:" + prop, "property_label": plabel,
                     "value": value, "value_label": vlabel, "note": note})

    g = f.get("gender") or f.get("sex")
    if g:
        v = SEX_VALUES.get(g.lower())
        if v: add(SEX_PROP, "Sex", "obo:" + v[0], v[1])
        else: add(SEX_PROP, "Sex", "", g, f"unrecognised value '{g}'")

    age = f.get("age")
    if age:
        nums = [int(n) for n in re.findall(r"\d+", age)]
        if nums:
            note = "" if re.fullmatch(r"\s*\d+\s*(-|–|to)?\s*\d*\s*", age) else f"original value '{age}'"
            add(MIN_AGE_PROP, "Actual Minimum Age of Subject", min(nums), note=note)
            add(MAX_AGE_PROP, "Actual Maximum Age of Subject", max(nums), note=note)
        else:
            add(MIN_AGE_PROP, "Actual Minimum Age of Subject", "", note=f"could not parse age '{age}'")

    country = next((v for k, v in f.items() if k.startswith("country")), None)
    if country:
        add(RESIDENCE_PROP, "Residence", country)   # free text, kept exactly as written
    return rows

SPEAKER_TAG = re.compile(r"^\s*([A-Z]{2,5}):")

def drop_speakers(text, speakers):
    """Blank out every turn by the given speakers (e.g. INT). A turn runs from its tag
    until the next line that starts with a speaker tag, so untagged continuation
    paragraphs belong to the same speaker. Text is replaced by spaces (newlines kept),
    so character offsets stay valid."""
    if not speakers:
        return text, 0
    out, dropping, n = [], False, 0
    for line in text.splitlines(keepends=True):
        m = SPEAKER_TAG.match(line)
        if m:
            dropping = m.group(1) in speakers
            n += dropping
        if dropping:
            line = "".join(c if c in "\r\n" else " " for c in line)
        out.append(line)
    return "".join(out), n

def clean_transcript(text):
    """Blank out speaker tags and transcription markup, keeping character offsets."""
    blank = lambda m: " " * len(m.group(0))
    text = re.sub(r"(?m)^\s*[A-Z]{2,5}:", blank, text)          # INT: / RES: speaker tags
    text = re.sub(r"\[[^\]\n]*\]", blank, text)                 # [unclear 0:02:19], [ph]
    text = re.sub(r"\((?:[A-Za-z]+\s?){1,3}\)", blank, text)     # (Laughs), (Clears throat)
    text = re.sub(r"(?<=\w)[’'](?:t|s|re|ve|ll|d|m)\b", blank, text)   # haven't -> haven (dropped below)
    return text

CONTRACTION_STEMS = {"haven", "hasn", "hadn", "isn", "aren", "wasn", "weren", "don", "doesn", "didn",
                     "couldn", "wouldn", "shouldn", "won", "can", "ain", "mustn", "needn"}

def keep_match(span, match_type, n_classes_in_onto, args):
    w = span.lower()
    if not args.no_filter:
        if w in CONTRACTION_STEMS:
            return False
        if w in STOPWORDS:
            return False
        if len(w) < args.min_length:
            return False
        # short synonyms are usually acronyms (NHS -> Nance-Horan syndrome); keep only if PREF
        if match_type == "SYN" and len(w) <= args.short_syn and " " not in w:
            return False
        # one span hitting many classes in one ontology = generic word ("yes" -> 300 NCIT classes)
        if n_classes_in_onto > args.max_classes:
            return False
    if args.pref_only and match_type != "PREF":
        return False
    return True

def get_json(url, apikey, params=None):
    if params:
        url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": f"apikey token={apikey}",
                                               "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

def fetch_labels(self_links, apikey, workers=8):
    """Look up prefLabel per class. (include=prefLabel on the annotator call
    triggers a server 500 for some inputs, so labels are fetched separately.)"""
    def one(link):
        try:
            return link, get_json(link, apikey, {"include": "prefLabel"}).get("prefLabel") or ""
        except Exception:
            return link, ""
    with ThreadPoolExecutor(workers) as ex:
        return dict(ex.map(one, self_links))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("-o", "--output", help="interview annotations CSV (default: <input>_annotations.csv)")
    ap.add_argument("-d", "--demographics-output",
                    help="demographics CSV (default: <input>_demographics.csv)")
    ap.add_argument("--ontologies", help="comma-separated acronyms (default: all)")
    ap.add_argument("--all-matches", action="store_true", help="keep overlapping shorter matches")
    ap.add_argument("--pref-only", action="store_true", help="keep only matches on preferred labels")
    ap.add_argument("--min-count", type=int, default=1, help="drop terms appearing fewer times")
    ap.add_argument("--min-length", type=int, default=3, help="minimum matched span length")
    ap.add_argument("--short-syn", type=int, default=4, help="drop synonym matches of this length or shorter")
    ap.add_argument("--max-classes", type=int, default=3,
                    help="drop a span that matches more than N classes within one ontology")
    ap.add_argument("--stopwords", help="file with extra stop words, one per line")
    ap.add_argument("--no-merge", action="store_true",
                    help="keep one row per ontology even when ontologies share the same class IRI")
    ap.add_argument("--drop-speakers", default="INT",
                    help="comma-separated speaker tags whose turns are removed before annotation "
                         "(default: INT; pass '' to keep everything)")
    ap.add_argument("--save-preprocessed", action="store_true",
                    help="also write the text actually sent to the annotator (<input>_preprocessed.txt)")
    ap.add_argument("--no-filter", action="store_true", help="disable all noise filters")
    ap.add_argument("--apikey", default=os.environ.get("EXPOPORTAL_APIKEY"))
    a = ap.parse_args()
    if not a.apikey:
        sys.exit("Set EXPOPORTAL_APIKEY or pass --apikey")
    text = open(a.input, encoding="utf-8").read()
    out = a.output or os.path.splitext(a.input)[0] + "_annotations.csv"
    header, text = split_header(text)
    participant = (re.search(r"PID_\d+", os.path.basename(a.input)) or
                   re.search(r".*", os.path.splitext(os.path.basename(a.input))[0])).group(0)
    demo_out = a.demographics_output or os.path.splitext(a.input)[0] + "_demographics.csv"
    demo = demographics(header, participant, a.apikey)
    with open(demo_out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["participant", "property", "property_label", "value", "value_label", "note"])
        w.writeheader(); w.writerows(demo)
    print(f"{len(demo)} demographic values -> {demo_out}")

    speakers = {x.strip() for x in a.drop_speakers.split(",") if x.strip()}
    text, n_turns = drop_speakers(text, speakers)
    if speakers:
        print(f"removed {n_turns} turns by {', '.join(sorted(speakers))}")
    if not a.no_filter:
        text = clean_transcript(text)
    if a.save_preprocessed:
        pre = os.path.splitext(a.input)[0] + "_preprocessed.txt"
        with open(pre, "w", encoding="utf-8") as f:   # collapse blanked lines for readability
            f.write(re.sub(r"\n\s*\n(\s*\n)+", "\n\n", "\n".join(l.strip() for l in text.splitlines())).strip() + "\n")
        print(f"preprocessed text -> {pre}")
    if a.stopwords:
        STOPWORDS.update(w.strip().lower() for w in open(a.stopwords, encoding="utf-8") if w.strip())

    results = annotate(text, a.apikey, a.ontologies, not a.all_matches)
    links = {r["annotatedClass"]["links"]["self"] for r in results if "links" in r["annotatedClass"]}
    labels = fetch_labels(links, a.apikey)

    # how many classes each (ontology, span position) maps to
    fan = {}
    for res in results:
        onto = res["annotatedClass"].get("links", {}).get("ontology", "").rstrip("/").split("/")[-1]
        for m in res.get("annotations", []):
            fan.setdefault((onto, m["from"], m["to"]), set()).add(res["annotatedClass"].get("@id"))

    # Aggregate per (ontology, class): count distinct text positions where it matched
    agg = {}
    for res in results:
        cls = res["annotatedClass"]
        onto = cls.get("links", {}).get("ontology", "").rstrip("/").split("/")[-1]
        key = (onto, cls.get("@id", ""))
        e = agg.get(key) or agg.setdefault(key, {"positions": set(), "spans": {}, "types": set(),
                                 "label": labels.get(cls.get("links", {}).get("self"), "")})
        for m in res.get("annotations", []):
            s, t = m["from"], m["to"]          # 1-based, inclusive
            if not keep_match(text[s - 1:t], m.get("matchType", ""), len(fan[(onto, s, t)]), a):
                continue
            if (s, t) in e["positions"]:       # same spot matched via PREF and SYN
                e["types"].add(m.get("matchType", "")); continue
            e["positions"].add((s, t))
            span = text[s - 1:t].lower()
            e["spans"][span] = e["spans"].get(span, 0) + 1
            e["types"].add(m.get("matchType", ""))

    rows = [{
        "ontology": o, "class_id": c, "pref_label": e["label"],
        "matched_terms": "; ".join(f"{k} ({v})" for k, v in
                                   sorted(e["spans"].items(), key=lambda x: -x[1])),
        "match_type": "/".join(sorted(e["types"])),
        "count": len(e["positions"]),
    } for (o, c), e in agg.items() if len(e["positions"]) >= a.min_count
       and (a.no_filter or not e["label"].lower().startswith(("obsolete", "deprecated")))]
    if not a.no_merge:   # same IRI imported into several ontologies (e.g. UBERON terms in EFO/MONDO) -> one row
        merged = {}
        for r in rows:
            m = merged.get(r["class_id"])
            if m is None:
                merged[r["class_id"]] = dict(r)
            else:
                m["ontology"] = ",".join(sorted(set(m["ontology"].split(",")) | {r["ontology"]}))
                m["pref_label"] = m["pref_label"] or r["pref_label"]
                if r["count"] > m["count"]:
                    m.update(count=r["count"], matched_terms=r["matched_terms"])
                m["match_type"] = "/".join(sorted(set(m["match_type"].split("/")) | set(r["match_type"].split("/"))))
        rows = list(merged.values())
    rows.sort(key=lambda r: (-r["count"], r["ontology"], r["pref_label"].lower()))
    fields = ["ontology", "class_id", "pref_label", "matched_terms", "match_type", "count"]
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)
    print(f"{len(rows)} terms ({sum(r['count'] for r in rows)} appearances) -> {out}")

if __name__ == "__main__":
    main()
