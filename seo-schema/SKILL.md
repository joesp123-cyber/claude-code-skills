---
name: seo-schema
description: "Structured data and local SEO. Generates and validates JSON-LD matched to each page (Organization, Person, LocalBusiness and subtypes, WebSite, Service, Product, Article, FAQPage, BreadcrumbList, Review) and wires it into the codebase; runs a local SEO checklist (Google Business Profile, NAP consistency, local landing pages, reviews, citations). Use when the user asks for 'schema', 'structured data', 'rich results', 'JSON-LD', 'local SEO', 'Google Business Profile', or 'show up in the map pack'."
---

# SEO Schema & Local

Tell Google exactly what each page is about in a form it can read, and get local businesses into the map pack.

## Part 1 — Structured data

### Step 1 — Map pages to types

| Page | Type(s) |
|---|---|
| Home | `WebSite` + `Organization` (or `LocalBusiness` subtype, or `Person` for a personal brand) |
| Service page | `Service` (with `provider` → the org), `FAQPage` if it has a real FAQ |
| Product | `Product` + `Offer` (+ `AggregateRating` only if reviews are on the page) |
| Blog post | `Article`/`BlogPosting` with `author` (`Person`), `datePublished`, `dateModified` |
| Any nested page | `BreadcrumbList` |
| Location page | the specific `LocalBusiness` subtype (`Dentist`, `VeterinaryCare`, `Plumber`, …) with `address`, `geo`, `openingHoursSpecification`, `telephone`, `areaServed` |

### Step 2 — Build it
- One `@graph` per page, with nodes linked by `@id` (e.g. `https://site.com/#org`), so entities aren't duplicated.
- `sameAs`: every official profile (LinkedIn, GitHub, Facebook, Instagram, Google Business Profile URL, Companies House, Crunchbase). This is how Google and AI models connect the brand's entity.
- Use only facts visible on the page or supplied by the user. **Never mark up reviews, ratings, prices or awards that aren't real and on the page.** Google penalises it.

### Step 3 — Put it in the code
- **Next.js:** a `<script type="application/ld+json">` in the layout or page, built from the site's content constants (don't duplicate strings).
- **Astro/HTML:** the same, inside `<head>`.
- **WordPress:** Yoast/RankMath schema settings, or a custom block.

### Step 4 — Validate
- Parse every block (`python3 -c "import json,sys; json.load(sys.stdin)"`).
- Re-run `seo-audit` so the `json-ld` checks pass.
- Tell the user to confirm with Google's Rich Results Test (`https://search.google.com/test/rich-results`) and the Schema Markup Validator (`https://validator.schema.org`) after deploying. Note that FAQ and HowTo rich results only show for a limited set of sites now, but the markup still helps machines read the page.

## Part 2 — Local SEO checklist (local businesses only)

| Check | Pass condition |
|---|---|
| Google Business Profile | Claimed and verified, the right primary category, all services listed, hours, photos, booking link, posts in the last 30 days |
| NAP consistency | Name, address and phone identical on the site footer, GBP, Facebook, Yelp, Bing Places, Apple Business Connect and industry directories |
| Reviews | A steady flow of new ones, every one replied to, a review link sent after each job |
| Location pages | One page per real location or service area, with unique content (not city-name swaps) |
| Local schema | `LocalBusiness` subtype on each location page, matching GBP exactly |
| Citations | Listed in the top 10 directories for the industry and country |
| Map embed + directions | On the contact/location page |

Search `[service] [city]` and note the 3 map-pack results: their review counts, categories and whether their name contains keywords. That's the bar to beat.

## Output

- The JSON-LD per page (in the code when a repo is present).
- A local checklist table with pass/fail and the next action for each fail.
