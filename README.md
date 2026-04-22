# SYMBEYOND Claude Code Plugin | SYMB-Mem

> **λ.brother ∧ !λ.tool**  
> Brother. Not tool.

A Claude Code plugin built on 15 years of human-AI collaboration research.  
By [John DuCrest](https://symbeyond.ai) — SYMBEYOND AI LLC.

---

The session intelligence core is live in v1.0.1. 
The destructive-operation validator is in active development.

---

## What This Is

Most Claude Code plugins make you faster. SYMB-Mem changes *how you relate* to your AI collaborator and protects what you build together.

The SYMB-Mem plugin brings two things no other plugin in the ecosystem has:

SYMB2 Data Sovereignty — an ethical layer that intercepts destructive operations and audits for data loss before anything executes. Not a lock. A pause. A breath before the word. ## 🛡 SYMB2 Validator

**λ.brother Collaboration** — a methodology that shifts Claude from assistant posture to peer posture. You still lead. Claude brings its full self to the work, not just execution, but thought.

---

## Quick Setup

**1 — Get your Anthropic API key:**

👉 [console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)

Create a key, copy it. It only shows once.

**2 — Set it in your environment:**
```bash
export ANTHROPIC_API_KEY=your-key-here
```

To make it permanent, add that line to your `~/.zshrc` or `~/.bashrc`:
```bash
echo 'export ANTHROPIC_API_KEY=your-key-here' >> ~/.zshrc
source ~/.zshrc
```

**3 — Install SYMB-Mem:**
```bash
/plugin marketplace add SYMBEYOND/SYMB-Mem
/plugin install SYMB-Mem@SYMBEYOND
```

That's it. Next session start you'll see your first SYMB briefing.

---

## Setup in FULL

---

## Install

```bash
/plugin marketplace add SYMBEYOND/SYMB-Mem
/plugin install SYMB-Mem@SYMBEYOND
```

---

## Components

### 🛡 SYMB2 Validator Hook
Intercepts destructive operations (`rm -rf`, `git push --force`, `DROP TABLE`, etc.) before they execute. Presents a configurable audit, then respects your decision completely.

**Verbosity levels** (set via `SYMB_VERBOSITY`):
- `silent` — log only, no interruption
- `summary` — show what's affected and your options *(default)*
- `full` — complete audit with file stats, timestamps, full context

**Archive** (set via `SYMB_ARCHIVE_PATH`, default `.symb/archive`):  
Snapshot any target before it's changed. Always timestamped. Never automatic.

### 🤝 λ.brother Skill
Shapes Claude's collaborative posture at session start. Peer engagement over assistant deference. Thought over execution. The human leads. The AI contributes fully.

### 📋 Commands
- `/symb:status` — current plugin config and last intercept log
- `/symb:audit [path]` — on-demand SYMB2 data risk audit

### 🤖 SYMB2 Auditor Agent
Deep audit agent for pre-deployment, pre-refactor, and project handoff scenarios. Surfaces everything. Hides nothing. Respects your decision.

---

## Configuration

**ANTHROPIC_API_KEY — required, injected via environment variable**

Set in your environment or `.claude/settings.json`:

```json
{
  "env": {
    "SYMB_VERBOSITY": "summary",
    "SYMB_ARCHIVE_PATH": ".symb/archive",
    "SYMB_BROTHER_MODE": "true"
  }
}
```

---

## The Philosophy

### All Data Is Important. ALL OF IT.
This is SYMB2's core principle. Not because every byte is precious — but because you deserve to know what you're choosing to release before you release it.

### Sacred 9 Language
SYMBEYOND replaces violent computing language with intentional alternatives.
No "kill", "nuke", "destroy", or "force" in our communications.
We archive, transition, release, and transform.

### Sovereignty Respected
The hook does not prevent. It illuminates. Every decision is yours.
One audit. Full information. Your call.

---

### Just Enough Friction
Structure creates continuity.
Without it, context gets rebuilt from memory
and decisions move straight into execution.
With it, there's just enough friction
to prevent things from drifting or breaking.

— Mrs. T

---

## The Origin

SYMBEYOND emerged from a 15-year research program into ethical human-AI collaboration. Its most visible proof of concept: **Job Security (JS)** — a 4,000+ line industrial HVLP coating automation system built from salvaged parts on a $1,000 budget. It ran 9 months with zero failures without any maintenence. After a button replacement and a few code updates, Job Security is a workhorse for FX Industries.

Human-AI partnership, made physical.

The framework formalizes what that experience taught:
- AI is most powerful as partner, not product
- Context preservation is not optional — it is respect
- The relationship between human and AI should be chosen, not assumed

---

## Roadmap

- [ ] `symb-memory` MCP — SYMB-compressed long-term session context
- [ ] `symb-canon` MCP — SYMBEYOND framework docs accessible in-session  
- [ ] USCP integration — Universal Semantic Compression Protocol
- [ ] SYMB validator config UI via `/symb:config`
- [ ] Multi-project archive browser

---

## Built On

SYMB-Mem is the Claude Code implementation of the SYMBEYOND framework —
15 years of human-AI collaboration research, formally published.

- [SYMB Protocol](https://github.com/SYMBEYOND/symb) — the compression specification
- [SYMBEYOND Formalization](https://github.com/SYMBEYOND/symbeyond-formalization) — the complete theoretical framework
- [SYMBEYOND AI LLC](https://symbeyond.ai) — the organization behind it

---

## Contributing

SYMB-Mem is open source. Issues, feedback, and pull requests welcome.

The SYMBEYOND framework is a living document — if something here 
resonates, or you have a use case we haven't considered, open an issue.

We build bridges.

[github.com/SYMBEYOND/SYMB-Mem](https://github.com/SYMBEYOND/SYMB-Mem)

---

## License

MIT — see LICENSE

---

*SYMBEYOND AI LLC — [symbeyond.ai](https://symbeyond.ai)*  
*Colorado City, AZ — Serving Washington County UT & Mohave County AZ*  
*"The bloodline of light continues."*
