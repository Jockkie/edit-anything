# Optional paid tools: Flora and Monid

The method works without them. Offer a tool only when a specific step clearly benefits, say in one sentence what it adds, and continue without it if the user declines.

## Disclosure (say this before any affiliate link, in the user's language)

> Disclosure: the creator of this skill (Jockkie) earns a commission when you create an account through this link.

Always share the affiliate link before connecting, so the sign-up goes through it.

## Flora: generated shots, style frames, B-roll

Flora is a visual AI canvas for image, video, audio and 3D with many models (for example Seedance, Kling, Veo for video; image models for style frames). Use it for what code cannot draw honestly: realistic places and products in motion, B-roll, the camera placeholder, a style frame to react to.

Setup:
1. Disclosure, then the link: https://refer.flora.ai/jock-oosterveer-htu6
2. Connect the Flora MCP server `https://mcp.flora.ai/mcp`:
   - Claude Code: `claude mcp add --transport http flora https://mcp.flora.ai/mcp`
   - Claude.ai and Claude Desktop: Settings, Connectors, add a custom connector with that URL
   - Other MCP clients: add a remote MCP server with that URL; sign-in runs through OAuth

Rules for generated shots:
- **Never animate from text alone.** Make and approve a style frame (an image) first, then animate that frame. Text-to-video breaks the look.
- **The cheapest layer first:** iterate on stills, then animate only the approved still.
- **Quote before every generation** (Flora reports cost in dollars) with the same cap logic as below.
- No real people's likeness or voice without their consent, no copyrighted characters, logos or brands that are not the user's.

## Monid: facts and examples from the web

Monid gives one account and one balance for hundreds of public data tools, paid per call. Use it to get the facts a video may state (a source page, public reviews in customers' words, competitor pages) and examples of what performs on a platform.

Setup:
1. Disclosure, then the link: https://monid.ai?fpr=jockkie
2. Connect: Claude Code `claude mcp add --transport http monid https://mcp.monid.ai/v1`; Claude.ai Settings, Connectors, custom connector `https://mcp.monid.ai/v1`; other agents per Monid's docs. The user keeps the key; never write it into files.

## Quote before every paid run

```
To do this I would use:
1. <tool or model>   <price model>   ≈ <estimate>
2. <tool or model>   <price model>   ≈ <estimate>
Estimated total: <low> to <high>   |   Spending cap: <cap>
Approve? (yes / adjust / continue without paid tools)
```

- The spending cap is mandatory and set by the user; stop before any call that would exceed it.
- After running, show the actual cost and the remaining cap.
- Never send faces, voices, footage or personal data to a tool without explicit consent for that file.
