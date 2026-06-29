---
name: frontend-design-workflow
description: "End-to-end workflow for creating production-quality frontend designs using wireframes, brainstorming, and the frontend-design plugin. Use this skill when the user wants to build a polished UI, website, landing page, web app, or component and wants a structured design process rather than jumping straight to code. Triggers when user mentions 'design workflow', 'wireframe to code', 'design process', 'UI design pipeline', 'frontend brainstorm', or when they want to go from idea → wireframe → design plan → production code. Also use when the user has a wireframe or mockup and wants to turn it into high-quality code, or when they want to improve the visual quality of an existing frontend."
---

# Frontend Design Workflow

A structured 5-step process for creating distinctive, production-grade frontends. Goes from idea → wireframe → brainstorm → design plan → polished code.

## Why This Workflow

Jumping straight from a description to code produces generic results. This workflow adds two critical steps — wireframing and brainstorming — that dramatically improve output quality by:
1. Separating **structure** (wireframe) from **aesthetics** (design plan)
2. Forcing deliberate design decisions before writing code
3. Making it easy to iterate on layout without rewriting code

## Prerequisites

### Required Plugins
If using Claude Code with Superpowers marketplace:
```
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
/plugin install frontend-design@claude-plugins-official
```

If using Claude.ai: the frontend-design skill should be available. The brainstorm step can be done manually in conversation.

### Key Reference
The Anthropic frontend aesthetics cookbook contains principles for avoiding generic "AI slop" design:
https://github.com/anthropics/claude-cookbooks/blob/main/coding/prompting_for_frontend_aesthetics.ipynb

Core principles from the cookbook:
- Choose a BOLD aesthetic direction (brutalist, maximalist, editorial, organic, etc.)
- Avoid generic fonts (Inter, Roboto, Arial) — pick distinctive, characterful fonts
- Dominant colors with sharp accents beat timid, evenly-distributed palettes
- One well-orchestrated page load animation creates more delight than scattered micro-interactions
- Unexpected layouts: asymmetry, overlap, diagonal flow, grid-breaking elements

## The 5-Step Process

### Step 1: Define the Brief

Before any design work, capture these essentials:

**What are we building?**
- Type: landing page / dashboard / web app / component / portfolio / form
- Purpose: what problem does it solve? who uses it?
- Content: what text, images, data needs to be shown?

**What's the vibe?**
Pick ONE dominant aesthetic direction:
- Brutally minimal
- Maximalist chaos
- Retro-futuristic
- Organic / natural
- Luxury / refined
- Playful / toy-like
- Editorial / magazine
- Brutalist / raw
- Art deco / geometric
- Soft / pastel
- Industrial / utilitarian
- Dark / moody
- Corporate / clean (avoid if possible — too generic)

**Technical constraints:**
- Framework: HTML/CSS/JS, React, Vue, Svelte?
- Responsive requirements?
- Accessibility needs?
- Must integrate with existing design system?

**Inspiration:**
- Any reference sites or designs they like?
- Brand colors or existing identity?
- Specific fonts or typography preferences?

### Step 2: Generate Wireframes

Wireframes define STRUCTURE without aesthetics. This is critical — it's much easier to describe layout changes on a wireframe than on a finished design.

**Tools for wireframing:**
- https://bareminimum.design/ — minimal wireframe generator
- Gemini with image generation — describe layout, get wireframe
- Excalidraw (excalidraw.com) — hand-drawn style, great for quick sketches
- Figma — if the user already uses it
- Even pen and paper → photo upload works

**What a good wireframe shows:**
- Layout structure (header, hero, sections, footer)
- Content hierarchy (what's biggest, what's secondary)
- Navigation structure
- Component placement (cards, forms, tables, charts)
- Responsive breakpoints (optional but helpful)

**What a wireframe does NOT show:**
- Colors, fonts, shadows, gradients
- Final copy / text
- Images or illustrations
- Animations or interactions

**If the user doesn't have a wireframe:**
Help them create one by asking about layout preferences, then generate a simple ASCII or SVG wireframe:

```
┌─────────────────────────────────┐
│  Logo          Nav    Nav   CTA │
├─────────────────────────────────┤
│                                 │
│      Hero Headline              │
│      Subtitle text              │
│      [Primary CTA] [Secondary] │
│                                 │
├─────────┬───────────┬───────────┤
│ Card 1  │  Card 2   │  Card 3  │
│ Icon    │  Icon     │  Icon    │
│ Text    │  Text     │  Text    │
├─────────┴───────────┴───────────┤
│      Feature Section            │
│  Image left  │  Text right     │
├─────────────────────────────────┤
│      Footer                     │
└─────────────────────────────────┘
```

### Step 3: Brainstorm Design Direction

This is where the magic happens. Take the brief + wireframe and explore creative directions.

**If using Claude Code with Superpowers:**
```
/superpowers:brainstorm
```
Feed it:
- The brief from Step 1
- The wireframe from Step 2
- Ask it to propose 2-3 distinct aesthetic directions
- Answer its clarifying questions

**If using Claude.ai (manual brainstorm):**

Ask Claude to propose design directions. Structure the conversation:

"Based on this wireframe and brief, propose 3 distinct design directions. For each, specify:
1. **Name** — a descriptive 2-3 word name
2. **Aesthetic** — the overall feel and mood
3. **Typography** — specific font pairing (display + body)
4. **Color palette** — 4-5 colors with hex codes
5. **Key visual element** — the ONE thing that makes it memorable
6. **Layout twist** — how it departs from the wireframe for visual interest
7. **Motion** — what animates and how"

**Evaluate and choose:**
The user picks one direction (or mixes elements from multiple). Get confirmation before proceeding.

### Step 4: Create the Design Plan

Consolidate everything into a concrete design plan document:

```markdown
# Design Plan: [Project Name]

## Aesthetic Direction
[Chosen direction with reasoning]

## Typography
- Display: [Font name] — [where to use, weight, size range]
- Body: [Font name] — [where to use, weight, size range]
- Source: Google Fonts / Adobe Fonts / system

## Color Palette
- Primary: #XXXXXX — [usage]
- Secondary: #XXXXXX — [usage]
- Accent: #XXXXXX — [usage]
- Background: #XXXXXX
- Text: #XXXXXX
- Muted: #XXXXXX

## Layout
[Description referencing wireframe sections]
- [Section]: [specific layout decisions]
- Responsive: [breakpoint strategy]

## Components
- Cards: [style description]
- Buttons: [style, hover states]
- Navigation: [style, behavior]
- [Other components...]

## Motion & Interaction
- Page load: [animation sequence]
- Scroll: [triggered effects]
- Hover: [micro-interactions]
- Transitions: [between states]

## Visual Details
- Background treatment: [gradients, patterns, textures]
- Shadows: [style and usage]
- Borders: [style and usage]
- Spacing rhythm: [base unit]

## The "One Thing"
[What makes this design memorable and unforgettable]
```

### Step 5: Generate Production Code

Take the design plan + wireframe and generate the actual code.

**If using Claude Code:**
```
/frontend-design:frontend-design
```
Feed it the design plan from Step 4 and the wireframe from Step 2.

**If using Claude.ai:**
Provide the design plan and wireframe, then ask Claude to generate the code. Include these instructions:

"Generate production-ready code following this design plan. Requirements:
- Single HTML file with embedded CSS and JS (or single React component)
- Use the exact fonts and colors specified
- Implement all animations described
- Make it responsive
- The design should be distinctive — avoid anything that looks AI-generated
- Pay meticulous attention to spacing, typography, and visual details
- Include real content (not lorem ipsum) where possible"

## Iteration

After the first version:

1. **Review** — Does it match the design plan? Is it memorable?
2. **Screenshot** — Take a screenshot and evaluate objectively
3. **Refine** — Identify specific elements to improve
4. **Regenerate** — Feed refinements back into the process

Common refinements:
- "The typography needs more contrast between heading and body sizes"
- "Add more whitespace between sections"
- "The animation on scroll is too subtle — make it more dramatic"
- "The color accent isn't visible enough — increase saturation"
- "This looks too corporate — push it more toward [aesthetic direction]"

## Quick Mode (Skip wireframing)

For small components or when the user already has a clear vision:

1. Get the brief (Step 1) — at minimum: what, vibe, constraints
2. Skip wireframe — describe layout in words
3. Brainstorm 2-3 directions (Step 3)
4. Pick one and go straight to code (Step 5)

This works for: single components, small sections, cards, forms, navbars.
NOT recommended for: full pages, multi-section layouts, complex dashboards.

## Anti-Patterns

- **Skipping the aesthetic choice** → results in generic design
- **Using "clean and modern" as a direction** → too vague, always produces the same thing
- **Starting with colors before layout** → leads to poor hierarchy
- **Using more than 2 fonts** → cluttered typography
- **Animating everything** → overwhelming, no focal point
- **Ignoring mobile** → always design mobile-first or at least responsive
- **Using stock patterns** → purple gradients on white, card grids with rounded corners, blue CTAs
