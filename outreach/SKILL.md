---
name: outreach
description: "Targeted outbound to business clients: builds the ideal client profile, finds 20–50 named businesses that fit (with the reason each fits), researches each for a personal hook and the right decision-maker, writes a LinkedIn sequence and a 3-email sequence per prospect, saves the emails as Gmail DRAFTS for review (never sends), and tracks everything in a CSV. Uses installed prospecting plugins (VibeLeads, Sales, FullEnrich, Vibe Prospecting) when present, otherwise public web research. Use when the user asks for 'outreach', 'find clients', 'LinkedIn outreach', 'cold email', 'prospect list', 'lead list for [industry]', or 'reach out to [type of business]'."
---

# Outreach — targeted business clients

Fewer, better-chosen prospects, each with a reason to reply. Quality beats volume, and protects the sender's domain and LinkedIn account.

## Input
1. **The offer:** what's sold, the outcome it delivers, proof (case studies, numbers with sources), and price range.
2. **Target:** business type + region (e.g. "independent vet clinics, North West England"), or "work it out from my offer".
3. **Sender:** name, role, sending email address (ideally a custom domain; see `email-brand`), LinkedIn profile URL.
4. **Volume:** default 20 prospects; 50 maximum per run.

## Step 1 — Ideal client profile (ICP)
Write it out and confirm it with the user before searching:
- Industry and subtype, size (staff or locations), region.
- **Trigger signals** that mean "needs this now": hiring for a related role, a new location, a bad review theme, an outdated site, a recent funding round, a new regulation, a competitor's move.
- Decision-maker titles (who signs) and the influencer (who feels the pain).
- Disqualifiers.

## Step 2 — Build the list
Use the best source available, in this order:
1. **Installed plugins:** VibeLeads (`b2b-prospecting`, `local-business-prospecting`, `hiring-signals`, `contact-enrichment`), Sales (`account-research`, `lead-triage`, `account-tiering`), FullEnrich or Vibe Prospecting. Say which one was used.
2. **Public web:** Google Maps/local results for local businesses, industry directories, Companies House (UK) or state registries, job boards (hiring signals), the company site's team or about page, LinkedIn company pages (view only).

For each company, record: name, site, location, size, **why it fits (the specific signal)**, and a score from 1 to 5 against the ICP. Drop anything under 3.

## Step 3 — Find the person and the hook
For each prospect:
- **Decision-maker:** name and title from the team page, LinkedIn or the registry. Get a business email only from the company's own site or an enrichment plugin. If unverified, mark it `UNVERIFIED`, and never guess patterns into the sending list.
- **Hook:** one specific, true, recent observation (their new branch, a job ad, a review theme, a gap on their site from a quick `seo-audit`, a post they wrote). This is the first line, and the reason they reply.

## Step 4 — Write the sequences

**LinkedIn (sent by hand by the user):**
1. Connection note, ≤300 characters: the hook plus why connecting makes sense. No pitch.
2. After they accept (day 2–3): a thank-you plus one useful thing (an insight or resource about *their* business), and a soft question.
3. Day 7–10: a short value message with a light call to action ("worth a 15-minute look?").
- Also: 2 comments to leave on their recent posts first, to warm the connection.

**Email (3 touches):**
1. Day 0: subject ≤5 words, lowercase-natural. Body ≤120 words: the hook → their likely problem → the outcome with proof → one easy call to action (a question, not a calendar link).
2. Day 3–4: a new angle or a mini case study, ≤80 words.
3. Day 8–10: the break-up / resource email, ≤60 words.
- Every email: a plain-text-looking format, no images or attachments, one link at most, the sender's full name and business address, and a one-line opt-out ("Not relevant? Reply 'no' and I won't follow up.").

Personalise every first line. Templates with only `{first_name}` swapped are spam.

## Step 5 — Save as Gmail drafts (never send)
If the Gmail connector is available (`mcp__Gmail__create_draft`), create **touch 1** for each verified prospect as a draft, with the subject and body ready, addressed to their email. Report how many drafts were created. **Never call send.** The user reviews and sends each one. Touches 2–3 go into the tracker for later.

## Step 6 — Tracker
Write `outreach-[segment]-[date].csv`:
`company,website,location,signal,icp_score,contact_name,title,email,email_status,linkedin_url,hook,li_connect_note,li_msg_2,li_msg_3,email_1_subject,email_1_body,email_2,email_3,status,next_action_date`

## Compliance (state it in the output)
- **UK:** PECR lets you cold email *corporate* addresses (ltd, plc, LLP) with an opt-out. Sole traders and partnerships count as individuals and need consent. UK GDPR: legitimate interest assessment, say where you got the data, honour opt-outs and erasure.
- **EU:** stricter in many member states (e.g. Germany) — check the country.
- **US (CAN-SPAM):** honest headers and subject, a physical address, a working opt-out honoured within 10 days.
- **LinkedIn:** its terms ban automation tools and scraping. Messages here are drafted for the user to send by hand. If they use a sending tool (e.g. WarmySender), say the account risk plainly and keep volumes low.
- Sending hygiene: a warmed custom domain with SPF, DKIM and DMARC (`email-brand`), ≤30–50 cold emails a day per inbox, and stop on any reply.

## Output
```
## Outreach — [segment]  (YYYY-MM-DD)
**ICP:** …   **Source used:** [plugin / public web]   **Prospects:** N (scored ≥3)
| # | Company | Why now (signal) | Contact | Hook | Score |
### Sample sequence (prospect #1, in full)
### Gmail drafts created: N (not sent)   Tracker: outreach-….csv
### Compliance notes
```

## Rules
- Never send email or LinkedIn messages yourself. Drafts only.
- Never invent contacts, emails, signals or case-study results. A prospect with no verifiable signal doesn't make the list.
- Never scrape LinkedIn or use automation against its terms.
