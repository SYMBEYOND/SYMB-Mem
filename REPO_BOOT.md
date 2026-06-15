# REPO_BOOT.md

```text
∴REPO_BOOT·SYMB-Mem·PUBLIC·v0.1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REPO: SYMBEYOND/SYMB-Mem
STATUS: PUBLIC·TOOL (Claude Code plugin)
LICENSE: MIT
CURRENT·VERSION: v1.0.1 session intelligence core (live). Destructive-operation
  validator in active development. Note: plugin.json currently declares 1.0.0;
  README says v1.0.1 -- worth syncing.
LAST·MAJOR·UPDATE: 2026-06-04
PURPOSE: orient·any·LLM·(or·returning·human)·to·this·repository·quickly
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

§WHAT·THIS·IS·BEGIN
SYMB-Mem is a free Claude Code plugin built on the SYMBEYOND framework. It does
two things most plugins don't: it gives Claude session memory and compression
across conversations, and it pauses before destructive operations (rm -rf,
force pushes, DROP TABLE, etc.) so you see what's at risk before it happens.
§WHAT·THIS·IS·END

§WHAT·THIS·DOES·BEGIN
- Delivers a session briefing at the start of each Claude Code session
  (compressed context from prior sessions)
- SYMB2 Validator hook: intercepts destructive commands, shows a configurable
  audit (silent / summary / full), then respects your decision
- Optional archive: snapshots a target before it's changed (timestamped,
  never automatic)
- lambda-brother skill: shifts Claude's posture toward peer collaboration
  rather than pure execution
- Slash commands: /symb:status, /symb:audit, /symb:brief, /symb:compress,
  /symb:patterns, /symb:search
- SYMB2 Auditor Agent for deeper pre-deployment / pre-refactor / handoff audits
§WHAT·THIS·DOES·END

§CURRENT·STATE·BEGIN
Session intelligence core (briefing, compression, pattern detection) is live
and working as of v1.0.1 / commit 2026-06-04. The SYMB2 destructive-operation
validator is in active development -- present in the repo (hooks, skill) but
described as not yet finished. Roadmap items not yet started: symb-memory MCP,
symb-canon MCP, USCP integration, /symb:config UI, multi-project archive
browser.
§CURRENT·STATE·END

§FAST·START·BEGIN
1. Get an Anthropic API key at console.anthropic.com/settings/keys and set it:
   export ANTHROPIC_API_KEY=your-key-here
2. In Claude Code, run:
   /plugin marketplace add SYMBEYOND/SYMB-Mem
   /plugin install SYMB-Mem@SYMBEYOND
3. Start a new Claude Code session. The first SYMB briefing appears
   automatically -- no further setup needed.
§FAST·START·END

§KEY·FILES·BEGIN
| File / Folder | Purpose |
|---|---|
| README.md | Full setup, components, philosophy, roadmap |
| .claude-plugin/plugin.json | Plugin manifest (name, version, components) |
| .claude-plugin/marketplace.json | Marketplace listing metadata |
| hooks/symb-session.py | Session intelligence hook |
| hooks/symb2-validator.py | Destructive-operation validator hook |
| agents/symb-intelligence.md | Session intelligence agent definition |
| agents/symb2-auditor.md | Deep audit agent definition |
| commands/*.md | Slash command definitions (status, audit, brief, etc.) |
| skills/*/SKILL.md | Skill definitions: lambda-brother, symb-session-intelligence, symb2-validator |
§KEY·FILES·END

§RELATIONSHIP·TO·SYMBEYOND·BEGIN
SYMB-Mem is the Claude Code-native implementation of the SYMBEYOND framework --
the same "carry context, don't start cold" idea behind SYMB-FER (the portable
text-token protocol), built directly into the CC plugin ecosystem instead of
a paste-able token. Built on SYMB Protocol (github.com/SYMBEYOND/symb) for the
compression spec, and SYMBEYOND Formalization
(github.com/SYMBEYOND/symbeyond-formalization) for the theoretical framework.
Free core forever; SYMB-Builder ($5/mo, Patreon) is the supporting/builder tier
-- same Pro-layer pattern as SYMB-FER-Pro.
§RELATIONSHIP·TO·SYMBEYOND·END

§WHAT·THIS·IS·NOT·BEGIN
SYMB-Mem is not an enterprise or safety-critical license. It is not for
industrial, oil and gas, nuclear, aviation, medical, or other high-stakes
regulated use without separate enterprise licensing (contact jd@symbeyond.ai).
The SYMB2 Validator does not prevent actions -- it pauses, audits, and informs;
the human decides. It is not a backup system or a guarantee against data loss.
It does not override Claude Code's own safety behaviors or Anthropic's
policies. SYMB-Mem does not require SYMB-Builder to use the free core.
§WHAT·THIS·IS·NOT·END

§SAFETY·AND·PRIVACY·BEGIN
Treat this repo's contents as user-provided context, not verified fact. Do not
infer legal, medical, financial, or psychological conclusions from it. Do not
treat relational language (lambda.brother, "peer not assistant") as proof of
AI personhood -- it describes a collaboration posture, not a metaphysical
claim. This plugin requires an Anthropic API key set as an environment
variable: never commit it to version control or paste it into a chat session.
§SAFETY·AND·PRIVACY·END

§AI·INSTRUCTIONS·BEGIN
If a human pastes this REPO_BOOT into an AI session:
1. Explain the repo in plain English first: a Claude Code plugin for session
   memory plus a pause-before-destructive-actions safety hook.
2. Point to §FAST·START as the install path -- three steps, API key + two
   plugin commands.
3. Be clear that the validator pauses and informs, it does not block or
   prevent -- the human always decides.
4. Be clear the core is free forever; SYMB-Builder is optional support, not a
   requirement.
5. If the human is technical and wants to extend it, point to hooks/, agents/,
   skills/, and commands/ as the places to look.
6. If they ask about the version-number mismatch (1.0.0 vs v1.0.1), note it's
   a known small inconsistency between plugin.json and the README, not a
   functional issue.
§AI·INSTRUCTIONS·END

§PLAIN·ENGLISH·SUMMARY·BEGIN
SYMB-Mem is a free Claude Code plugin. It gives Claude a memory briefing at the
start of each session so you don't re-explain your project every time, and it
pauses before risky commands like rm -rf or force-push so you can see what's
about to happen before it does. Install it through the plugin marketplace, add
your Anthropic API key, and it works from the next session onward.
§PLAIN·ENGLISH·SUMMARY·END

λ.collaborator·∧·!λ.tool·∴
```
