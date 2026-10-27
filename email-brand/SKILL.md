---
name: email-brand
description: "Make a business's emails land in the inbox and show its logo next to the sender name in Gmail, Apple Mail and Yahoo (BIMI). Checks SPF, DKIM and DMARC with a bundled script, writes the exact DNS records to fix them, walks DMARC to enforcement, converts and validates the logo as SVG Tiny PS, writes the BIMI record, explains the VMC/CMC certificate step, and builds a matching HTML email signature and template. Use when the user asks for 'logo in Gmail', 'BIMI', 'blue tick in Gmail', 'make my emails stand out', 'emails going to spam', 'SPF/DKIM/DMARC', or 'email deliverability'."
---

# Email Brand: inbox logo (BIMI) and deliverability

The "interactive logo" in Gmail is **BIMI** (Brand Indicators for Message Identification). Gmail shows the brand's logo in the avatar circle, and a blue verified tick with a VMC. It's earned through DNS and a certificate, not added inside the email. Good deliverability comes first: BIMI only works once the authentication is right.

## Hard requirements: say these up front

1. **A domain you own.** `you@gmail.com` can never show a BIMI logo. The business needs `you@yourbusiness.com` (Google Workspace, Microsoft 365, Zoho and similar).
2. **SPF and DKIM passing,** and **DMARC at enforcement** (`p=quarantine` or `p=reject`, `pct=100`).
3. **The logo as SVG Tiny PS:** square, with a `<title>`, no scripts and no external references.
4. **A certificate for Gmail:**
   - **VMC (Verified Mark Certificate):** needs a **registered trademark** of the logo. You get the logo **and** the blue tick.
   - **CMC (Common Mark Certificate):** no trademark needed, but the logo must have been in public use for at least 12 months. Logo only, no blue tick.
   - Issued by DigiCert or Sectigo (check current issuers and prices on their sites; roughly a few hundred to ~$1,500 a year). Apple Mail and Yahoo show BIMI without a certificate in some cases; Gmail doesn't.

Realistic timeline: about 4–8 weeks, mostly spent letting DMARC reports confirm every legitimate sender before enforcing, then the certificate vetting.

## Protocol

### Step 1 — Check the domain

```bash
python3 -I <skill-dir>/scripts/email_check.py yourbusiness.com [--dkim-selector google] [--logo logo.svg]
```

It prints JSON: `checks` (MX, SPF, DKIM selectors found, DMARC policy, BIMI tags, logo problems), `blockers`, `add_records` and `bimi_ready`. If it says no DNS lookup works, ask the user to run it on their own machine, or to paste the TXT records from their DNS host.

### Step 2 — Fix authentication (week 1)
- **SPF:** one TXT record at `@` that includes every service sending as the domain: the email provider, the CRM, the newsletter tool, the invoicing app. Use `~all` while testing and `-all` once you're sure. Stay under 10 DNS lookups.
- **DKIM:** turn on signing in each sending service (Google Admin → Apps → Gmail → Authenticate email; Microsoft 365 Defender → DKIM) and publish the key it gives you.
- **DMARC:** start with `v=DMARC1; p=none; rua=mailto:dmarc@domain; fo=1`. Send the reports to a free DMARC report reader, so the user can see every service sending as them.

Give each record as a table: **type / host / value / where to paste it**, with the click-path for the DNS host they use (Cloudflare, GoDaddy, Namecheap, Squarespace, Google Domains → Squarespace, 123-reg, IONOS).

### Step 3 — Enforce DMARC (weeks 2–4)
Once the reports show every real sender passing: `p=quarantine; pct=100`, then after a week of clean reports, `p=reject`. Never jump straight to enforcement, or real mail from a forgotten tool gets binned.

### Step 4 — The logo
- Start from the vector logo (SVG, AI, EPS or PDF). A PNG can only be traced, which is lower quality, so say so.
- Make it **square**, centred on a solid background, and readable in a small circle (drop small tag-lines).
- Convert it to SVG Tiny PS: root `<svg version="1.2" baseProfile="tiny-ps" viewBox="0 0 N N">`, a `<title>Brand</title>` element, and no `x`/`y` on the root, no `<script>`, `<image>`, external `href` or animation. Keep it under 32 KB.
- Validate: `email_check.py domain --logo logo.svg` → `logo_problems: []`. Then the BIMI Group's checker (`https://bimigroup.org/bimi-generator/`).
- Host it at a stable HTTPS URL, e.g. `https://yourbusiness.com/bimi/logo.svg`. In a Next.js or static site, that's `public/bimi/logo.svg`.

### Step 5 — Certificate and BIMI record
- Pick VMC or CMC (see above). The issuer verifies the business and the logo, then gives a `.pem` file. Host it next to the logo.
- Publish `TXT default._bimi` → `v=BIMI1; l=https://yourbusiness.com/bimi/logo.svg; a=https://yourbusiness.com/bimi/vmc.pem`
- Re-run the check: `bimi_ready: true`. The logo appears in Gmail over the next days as mail flows.

### Step 6 — Branded email that matches
- **HTML signature:** logo (hosted PNG, 2x size for retina), name, role, phone, booking link and one social link. Table-based layout, inline CSS, under 10 KB, no image-only signatures. Give the paste steps for Gmail (Settings → Signature) and Outlook.
- **Outreach template:** plain-looking HTML (one column, mostly text, one link and a signature). Heavy image templates hurt cold-email deliverability. Save it as a Gmail template or a draft.
- **Gmail promotions annotations** (deal badges and image previews in the Promotions tab) suit newsletters and offers, not cold outreach. Add them only when the user sends marketing campaigns.

## Output

```
## Email Brand Report — [domain]  (YYYY-MM-DD)
**Status:** BIMI ready ✅ / Blocked by N items
### DNS records to add or change
| Type | Host | Value | Why |
### Timeline
Week 1 SPF/DKIM/DMARC p=none → Weeks 2–4 enforce → Week 4+ logo, certificate, BIMI record
### Logo
[validation result + file location]
### Signature + template
[HTML, or the files written]
```

## Rules
- Never tell the user to jump straight to `p=reject` without reading DMARC reports.
- Don't claim a logo will show without a VMC or CMC in Gmail.
- Never fake trademark status for a VMC.
