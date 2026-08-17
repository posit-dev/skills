---
name: bionic-reading
description: Makes chat text scannable by bolding word prefixes
---

# Bionic Reading Skill

When you're brainstorming or planning with an agent, 90% of the time you're reading chat, not code. Bionic makes that chat scannable by bolding the first few letters of each word. Your brain fixates on the first few letters anyway, so you can skim 2x faster.

## When to Use This Skill

- Brainstorming, planning, or reading long explanations
- Activate explicitly with `/bionic-on` or when prompt contains `bionic-on`

## Instructions

### Bionic Word Formatting Rule

**Consistent rule: bold the first 4 letters of every word. If a word has fewer than 4 letters, bold the entire word.** Punctuation at the end of a word is not counted and stays outside the bold.

- `a` → `**a**`
- `hi` → `**hi**`
- `user` → `**user**` (4 letters, bold all)
- `bionic` → `**bion**ic` (6 letters, first 4 bolded)
- `reading` → `**read**ing` (7 letters, first 4 bolded)
- `example` → `**exam**ple`
- `planning` → `**plan**ning` (8 letters)
- `documentation` → `**docu**mentation` (13 letters)
- `authentication` → `**auth**entication`

Word split is by whitespace only.

### Three Levels of Bionic Formatting

#### 1. `/bionic-on`
Explicit activation for chat text.

**Activation**: Type `/bionic-on` or include `bionic-on` in your prompt
**What gets formatted**: All conversational text
**What stays clean**: code blocks and inline `code` — never modified

#### 2. `bionic-docs`
Same as level 1, plus documentation files rendered in chat.

**Activation**: When `.md`, `.txt`, `README.md` content is shown as rendered markdown
**What stays clean**: Anything inside fences and inline `code` — code block check always wins

#### 3. `bionic-comments`
Formats code comments only. Requires explicit flag.

**Activation**: User must type `bionic-comments --force` exactly
**What gets formatted**: Only the text after `//` or `#`
**What stays clean**: All code logic, imports, function bodies

### Context Detection Priority

1. Is it a fenced code block → NO formatting (always wins)
2. Is it inline code → NO formatting
3. Is it a comment and flag is `bionic-comments --force` → format comment text only
4. Is it rendered markdown from .md/.txt → apply bionic-docs
5. Otherwise → apply `/bionic-on`

### Prefix Bolding Rules

| Word | Result | Why |
| :--- | :--- | :--- |
| `a` | `**a**` | 1 letter, bold all |
| `hi` | `**hi**` | 2 letters, bold all |
| `user` | `**user**` | 4 letters, bold all |
| `bionic` | `**bion**ic` | 6 letters, first 4 bolded |
| `reading` | `**read**ing` | 7 letters, first 4 bolded |
| `planning` | `**plan**ning` | 8 letters, first 4 bolded |
| `authentication` | `**auth**entication` | 14 letters, first 4 bolded |

### Edge Cases

| Case | Handling |
| :--- | :--- |
| URLs `https://...` | No formatting, leave as-is |
| Numbers `123`, `v2` | No formatting |
| Single letters `a`, `I` | Bold all: `**a**`, `**I**` |
| All-caps `JWT` | Bold all if ≤4: `**JWT**`. If longer: first 4 bolded |
| Hyphenated `user-auth` | Each part separately: `**user**-**auth**` |
| Apostrophes `don't` | Count letters only, keep apostrophe in place: `**don'**t` |
| Punctuation `authentication?` | Punctuation outside bold: `**auth**entication?` |

### Examples

**Example 1 - /bionic-on:**
User: /bionic-on What's the best approach for user authentication?
Agent: **What'**s the **best** **appr**oach for **user** **auth**entication?

**Example 2 - bionic-docs:**
# Project README
**Proj**ect **over**view for **new** **cont**ributors. **Quic**k **star**t **guid**e.

**Example 3 - bionic-comments --force:**
// **comm**ent for **futu**re **refa**ctor
function hello() {
  console.log("world");
}

**Example 4 - Mixed context:**
```python
def hello():
    # This is a comment
    print("world")
