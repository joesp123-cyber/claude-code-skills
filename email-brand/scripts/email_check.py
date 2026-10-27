#!/usr/bin/env python3
"""Check a sending domain's email authentication and BIMI readiness.

    python email_check.py example.com
    python email_check.py example.com --dkim-selector google --logo logo.svg

Looks up MX, SPF, DKIM, DMARC and BIMI, then says what blocks the logo from
showing in Gmail and which DNS records to add. DNS goes through `dig`, then
`nslookup`, then DNS-over-HTTPS, whichever works. Standard library only.
Prints JSON.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import urllib.request
import xml.etree.ElementTree as ET

COMMON_SELECTORS = ["google", "selector1", "selector2", "default", "k1", "k2", "s1", "s2", "mail", "dkim", "smtp", "mxvault", "zoho"]


def _dig(name, rtype):
    out = subprocess.run(["dig", "+short", rtype, name], capture_output=True, text=True, timeout=10).stdout
    return [_join_txt(l) if rtype == "TXT" else l.strip() for l in out.splitlines() if l.strip()]


def _nslookup(name, rtype):
    out = subprocess.run(["nslookup", f"-type={rtype}", name], capture_output=True, text=True, timeout=10).stdout
    if rtype == "TXT":
        return [_join_txt(m) for m in re.findall(r'text = ((?:"[^"]*"\s*)+)', out)]
    return [m.strip() for m in re.findall(r"mail exchanger = (.+)", out)]


def _doh(name, rtype):
    url = f"https://dns.google/resolve?name={name}&type={rtype}"
    with urllib.request.urlopen(url, timeout=10) as r:
        data = json.load(r)
    return [_join_txt(a["data"]) if rtype == "TXT" else a["data"] for a in data.get("Answer", [])]


def _join_txt(s):
    """'"v=spf1 a" "-all"' -> 'v=spf1 a-all' (TXT strings concatenate with no separator)."""
    parts = re.findall(r'"((?:[^"\\]|\\.)*)"', s)
    return "".join(parts) if parts else s.strip()


def make_resolver():
    tried = []
    for name, fn, needs in (("dig", _dig, "dig"), ("nslookup", _nslookup, "nslookup"), ("dns-over-https", _doh, None)):
        if needs and not shutil.which(needs):
            continue
        try:
            fn("google.com", "MX")
            return name, fn
        except Exception as e:  # try the next method
            tried.append(f"{name}: {e}")
    raise SystemExit("no working DNS lookup (" + "; ".join(tried or ["dig/nslookup not installed"]) + ")")


def parse_tags(record):
    return {k.strip().lower(): v.strip() for k, _, v in (p.partition("=") for p in record.split(";")) if k.strip()}


def check_svg(path):
    """Gmail wants SVG Tiny Portable/Secure: tiny-ps profile, a <title>, square, nothing external."""
    problems = []
    try:
        root = ET.parse(path).getroot()
    except Exception as e:
        return [f"not parseable XML: {e}"]
    if root.get("baseProfile") != "tiny-ps":
        problems.append('root <svg> needs baseProfile="tiny-ps"')
    if root.get("version") != "1.2":
        problems.append('root <svg> needs version="1.2"')
    if root.find("{http://www.w3.org/2000/svg}title") is None and root.find("title") is None:
        problems.append("needs a <title> element with the brand name")
    for attr in ("x", "y"):
        if root.get(attr) is not None:
            problems.append(f"root <svg> must not have an {attr} attribute")
    vb = (root.get("viewBox") or "").split()
    if len(vb) == 4 and abs(float(vb[2]) - float(vb[3])) > 0.01:
        problems.append("logo must be square (viewBox width == height)")
    with open(path, encoding="utf-8", errors="replace") as f:
        raw = f.read()
    if re.search(r"<script|<image|<foreignObject|\son\w+=", raw, re.I):
        problems.append("no scripts, embedded raster <image>, foreignObject or event handlers allowed")
    if re.search(r'(?:xlink:)?href="(?:https?:)?//', raw):
        problems.append("no external references")
    if len(raw.encode()) > 32 * 1024:
        problems.append("keep the file under 32 KB")
    return problems


def evaluate(domain, rec, selectors, logo):
    """rec: dict of lookups already done. Returns the report. Kept separate from DNS so it can be tested."""
    out = {"domain": domain, "checks": {}, "blockers": [], "add_records": []}
    c = out["checks"]

    c["mx"] = rec["mx"]
    if not rec["mx"]:
        out["blockers"].append("No MX records: the domain can't receive mail, and receivers distrust it.")

    spf = [t for t in rec["txt"] if t.lower().startswith("v=spf1")]
    c["spf"] = spf
    if not spf:
        out["blockers"].append("No SPF record.")
        out["add_records"].append({"type": "TXT", "host": "@", "value": "v=spf1 include:_spf.google.com ~all",
                                   "note": "Google Workspace shown; use your provider's include."})
    elif len(spf) > 1:
        out["blockers"].append("Multiple SPF records: merge them into one, or SPF fails.")
    else:
        lookups = len(re.findall(r"\b(include:|a\b|a:|mx\b|mx:|ptr|exists:|redirect=)", spf[0]))
        c["spf_dns_lookups_approx"] = lookups
        if lookups > 10:
            out["blockers"].append("SPF needs more than 10 DNS lookups, so it will fail: flatten it.")
        if spf[0].rstrip().endswith("+all"):
            out["blockers"].append("SPF ends in +all, which lets anyone send as you.")

    found = {s: v for s, v in rec["dkim"].items() if v}
    c["dkim_selectors_found"] = sorted(found)
    if not found:
        out["blockers"].append(f"No DKIM key found for selectors {selectors}. Turn on DKIM signing in your email provider, then publish its key.")

    dmarc = [t for t in rec["dmarc"] if t.lower().startswith("v=dmarc1")]
    c["dmarc"] = dmarc
    if not dmarc:
        out["blockers"].append("No DMARC record. Bulk senders need one, and BIMI needs it at enforcement.")
        out["add_records"].append({"type": "TXT", "host": "_dmarc", "value": f"v=DMARC1; p=none; rua=mailto:dmarc@{domain}; fo=1",
                                   "note": "Start at p=none for 2-4 weeks and read the reports, then move to quarantine, then reject."})
    else:
        tags = parse_tags(dmarc[0])
        p, pct, sp = tags.get("p", "none"), tags.get("pct", "100"), tags.get("sp")
        c["dmarc_policy"] = {"p": p, "pct": pct, "sp": sp, "rua": tags.get("rua")}
        if p not in ("quarantine", "reject") or pct != "100" or sp == "none":
            out["blockers"].append(f"DMARC is not at enforcement (p={p}, pct={pct}, sp={sp}). BIMI needs p=quarantine or p=reject with pct=100.")
            out["add_records"].append({"type": "TXT", "host": "_dmarc",
                                       "value": f"v=DMARC1; p=quarantine; pct=100; rua={tags.get('rua') or f'mailto:dmarc@{domain}'}; fo=1",
                                       "note": "Only after the reports show all your real senders passing SPF or DKIM."})
        if not tags.get("rua"):
            out["blockers"].append("DMARC has no rua= address, so you're getting no reports on who sends as you.")

    bimi = [t for t in rec["bimi"] if t.lower().startswith("v=bimi1")]
    c["bimi"] = bimi
    if not bimi:
        out["add_records"].append({"type": "TXT", "host": "default._bimi",
                                   "value": f"v=BIMI1; l=https://{domain}/bimi/logo.svg; a=https://{domain}/bimi/vmc.pem",
                                   "note": "Gmail shows the logo only with a VMC or CMC certificate (the a= URL)."})
        out["blockers"].append("No BIMI record.")
    else:
        tags = parse_tags(bimi[0])
        c["bimi_tags"] = tags
        if not tags.get("a"):
            out["blockers"].append("BIMI record has no a= certificate. Gmail won't show the logo without a VMC or CMC.")
        if not tags.get("l", "").startswith("https://"):
            out["blockers"].append("BIMI l= must be an https URL to an SVG Tiny PS file.")

    if logo:
        c["logo_problems"] = check_svg(logo)
        if c["logo_problems"]:
            out["blockers"].append("Logo is not valid SVG Tiny PS: " + "; ".join(c["logo_problems"]))

    out["bimi_ready"] = not out["blockers"]
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("domain")
    ap.add_argument("--dkim-selector", action="append", help="DKIM selector to check (repeatable); defaults to common ones")
    ap.add_argument("--logo", help="local SVG to validate as SVG Tiny PS")
    args = ap.parse_args()
    d = args.domain.lower().strip().removeprefix("https://").removeprefix("http://").strip("/")
    if d in ("gmail.com", "googlemail.com", "outlook.com", "hotmail.com", "yahoo.com", "icloud.com"):
        raise SystemExit(f"{d} is a free mailbox provider. BIMI needs a domain you own (e.g. you@yourbusiness.com).")

    method, look = make_resolver()

    def q(name, rtype):
        try:
            return look(name, rtype)
        except Exception:
            return []

    selectors = args.dkim_selector or COMMON_SELECTORS
    rec = {
        "mx": q(d, "MX"),
        "txt": q(d, "TXT"),
        "dmarc": q(f"_dmarc.{d}", "TXT"),
        "bimi": q(f"default._bimi.{d}", "TXT"),
        "dkim": {s: [t for t in q(f"{s}._domainkey.{d}", "TXT") if "p=" in t] for s in selectors},
    }
    report = evaluate(d, rec, selectors, args.logo)
    report["dns_method"] = method
    json.dump(report, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
