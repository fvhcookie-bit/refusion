# Clean-room protocol of the ReFusion project

Русская версия: [docs/ru/process/README.md](../ru/process/README.md)

The goal is to write our own implementation of Wipeout Fusion so that it contains nothing taken from the original's code:
neither program text, nor its internal structure, nor names. To this end the work is divided between two isolated
groups, and the only channel between them is the written specification `spec/`, checked for "contamination".

> This is an engineering practice that reduces risk and provides evidence of independence, not a legal guarantee.
> Game assets (tracks, models, sound, texts) and trademarks are a separate matter: the implementation **does not contain** them
> and works with files that the user takes from their own copy of the game.

## 1. Roles

| role | what it does | what it has access to |
|---|---|---|
| **Dirty team** (researchers) | reverse engineering, recordings and observation of the running game; writes and corrects `spec/` | everything: the executable, decompilation, private notes, memory of the running game, tools |
| **Editor** (contamination controller) | checks every change to `spec/` against the [checklist](review_checklist.md), passes or returns it; keeps the logs | `spec/`, `process/`, and during review the private notes (only to understand where a fact comes from) |
| **Clean team** (implementation) | writes code from `spec/`, asks questions through the editor | **only** a specification release (`spec/` + `process/`) and a legally purchased game |
| **Recording operator** | runs the game and the recording tools, plays the required races as assigned by the researcher | the recording tools as a "black box"; does **not** read their output, the private notes or technical reports |

One person cannot be in both the dirty and the clean team at once. Anyone who has **studied** the private notes, decompilation or
disassembly of this game is in the dirty team for this project. A fleeting contact without understanding (leafed through a file,
opened a disassembler and understood nothing) does not make a person dirty, but is **recorded** in the private admission log
(not published). The editor may coincide with a researcher, but then changes to `spec/` must additionally be reviewed
by a second person (two-key rule).

### Recording operator
A member of the clean team may be a recording operator — then data for the dirty team is collected by his hands, but no knowledge
passes to him. Conditions:
- he receives assignments in terms of the game ("drive a lap of Florion 2F without touches", "start recording before the start");
- he does not open memory recordings, recording tool output or private notes; he only carries files to where the researcher will take them;
- if something dirty still catches his eye — an entry in the private admission log (kept by the editor, not part of the public release).

### AI assistants
The same rules apply to AI assistants as to people, at the level of the **working session**:
- a session that had this whole repository, the private notes, decompilation or reverse-engineering tool output in its context is dirty;
- implementation is to be done in a **separate repository** into which only a specification release is copied (section 4).
  Do not connect this repository to the implementation session, and do not mix implementation with reverse engineering in one session;
- if the assistant itself wrote `spec/` from the private notes, it worked as the dirty team; the result is checked by the editor;
- a dirty session that communicates with a member of the clean team (for example with the recording operator) writes to him only
  assignments and conclusions in terms of behaviour, and everything technical goes into the private notes.

## 2. What the clean team may and may not do

**May:**
- read a specification release, ask questions through the question log ([`spec/QUESTIONS.md`](../spec/QUESTIONS.md));
- play their legal copy of the game, record video, look at the screen (HUD, menus, lap times);
- read the game's **data files** (`SHIPS.INI`, `WEAPONSTATS.INI`, `.TRK`, `GAME.BNI` etc.) — the formats are described in `spec/07`;
- use publicly available documentation on formats (MPEG-2, TGA etc.) and on the PS2 as a platform.

**May not:**
- open the game's executable in a disassembler/decompiler, read its strings and tables;
- read the research's private notes, decompilation, disassembler projects, scripts and reverse-engineering tool output;
- read the memory of the running game (memory viewers and a disassembler) — that is observing the internals, not the behaviour;
- take code from other people's decompilations, recompilations and source leaks of this game;
- read the code and patches of game modifications and tools made by the dirty side, **including published ones**:
  they contain addresses and the structure of the original. Using a ready-made modification in the game is allowed;
- receive anything from the dirty team bypassing the specification and the question log (verbally, in chats, "in secret").

## 3. How a fact gets into the specification

1. The dirty team establishes a fact (code, race recording, observation) and writes the evidence into the private notes.
2. It formulates the rule in `spec/` **in its own words as behaviour**: what is observed, which numbers, in which order.
   It does not rewrite a function line by line, does not keep the names of variables, branches and memory structures of the original
   if they are not needed for the observable result.
3. It gives the rule an ID (`PHY-6`, `WPN-12` …) and an evidence mark `[✓]`/`[code]`/`[?]`.
4. It adds a row to the private traceability log (not published): ID → where the evidence is.
5. It runs the automatic check: `python docs/process/check_spec.py`.
6. The editor checks the change against the [checklist](review_checklist.md) and notes the release in [`spec/CHANGELOG.md`](../spec/CHANGELOG.md).

## 4. Releasing the specification to the clean team

The clean team receives **not the repository** (it holds the private notes and the whole history), but an archive of the checked release:

```sh
git tag spec-r1                       # after the editor's check
git archive --format=zip -o refusion-spec-r1.zip spec-r1 docs/spec docs/process
```

The archive is unpacked into a separate implementation repository. Releases are numbered `r1, r2, …`; changes
are listed in `spec/CHANGELOG.md` so that the clean team can see which rules changed.

## 5. Clean team questions

- A question is written in [`spec/QUESTIONS.md`](../spec/QUESTIONS.md) with ID `Q-NNN` and is phrased about **behaviour**
  ("what happens if a ship picks up a weapon while holding fire?"), not about code.
- The dirty team answers with a **change to the specification** (a new or refined rule) and a reference to its ID.
  The answer "not known" is also an answer: the rule goes to `spec/08_open_questions.md`.
- The answer goes through the same editor check as any change to `spec/`.

## 6. Checking the implementation against the original

The clean team does not look into the original's memory, so the bit-exact comparison is done by the dirty team:
1. the clean team passes an input recording and the output of its implementation (positions, speeds, shield by frame);
2. the dirty team runs the same input on the original game and compares;
3. the answer comes back **only** in terms of the specification: "matches" or "diverges in rule PHY-9 from frame N:
   X is observed, you have Y". No addresses, field names or code fragments.

Test cases that can be checked without running the original are in [`spec/09_test_cases.md`](../spec/09_test_cases.md).

## 7. Logs (the evidence base of independence)

| log | where | kept by |
|---|---|---|
| admission of participants and their declarations | private admission log (not published) | editor |
| questions and answers | [`spec/QUESTIONS.md`](../spec/QUESTIONS.md) | editor |
| specification releases and checks | [`spec/CHANGELOG.md`](../spec/CHANGELOG.md) | editor |
| traceability of rules to evidence | private traceability log (not published) | dirty team |

Logs are not rewritten retroactively: corrections go in as a new line. The git history keeps the dates.

## 8. Implementation plan

The order of the implementation work is determined by the clean team.

## 9. If contamination has occurred

If prohibited material got into a release or a clean team member saw dirty data:
1. record the incident in the admission log (what, who, when);
2. correct the specification and issue a new revision;
3. the code that the participant wrote after contact with dirty data **in the affected area** is rewritten by another
   clean team member from the corrected specification.

### Audit of implementation code
If a clean team member has recorded contacts with dirty data (see the admission log), before each release
of the implementation the dirty side checks its code for "echoes" of the original: memory addresses and offsets, the order and layout of fields,
internal names, constants that are not in `spec/`, function structure that repeats the original. The answer is only "clean" or
"in file X, line N — a value/structure that is not in the specification; where does it come from?". What is found is rewritten from
the specification. The audit result is recorded in the admission log.
