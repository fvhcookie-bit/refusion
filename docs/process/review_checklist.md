# Checklist for reviewing the specification for contamination

The editor goes through it for **every** change to `spec/` before release. The automatic part is
`python docs/process/check_spec.py`; it catches the obvious but does not replace reading with your own eyes.

## A. Forbidden in `spec/` (returned without discussion)
- [ ] Memory and code addresses of the original (like `0x1A2B3C`), offsets of **structure fields in memory** (`ship + 0x...`).
      Offsets inside **files** (`.TRK`, `GAME.BNI`, the save) are allowed: that is a data format.
- [ ] Disassembly, decompiler pseudocode, fragments of the original's code in any form, including a "line-by-line retelling".
- [ ] Internal names of the original: functions, variables, fields, classes, source files, debug labels —
      even transliterated or slightly altered. Signs: `_Q`, `g_`, `FUN_`, `DAT_`, `CamelCase_With_Underscore`,
      `.cpp`, field names like `fooBarBaz`.
- [ ] Strings that exist **only in the executable** (debug messages, enum names), except text that the
      player sees on screen and names from data files.
- [ ] Names of and references to closed research materials: notes, decompilation, reverse-engineering tools, save numbers.
- [ ] Bit values of internal flags and memory masks (bits in **files** are fine).

## B. Check by meaning
- [ ] The rule describes **behaviour** (input → observable result), not the structure of the code. The order of steps is given only
      if it affects the result, and this is stated.
- [ ] New terms come from the game data, from the screen, or are descriptive; they are in the glossary (`spec/00_glossary.md`).
- [ ] The rule has an ID and a `[✓]` / `[code]` / `[?]` mark; for `[✓]` the parentheses say what confirmed it (no addresses).
- [ ] For each new ID there is a row in the closed traceability log (not published).
- [ ] Constants and tables are minimal, as needed for the result. Large tables from the executable are not carried over
      in full without need; if they cannot be avoided, it is marked where they "mechanically" come from (for example, "from a data file").
- [ ] No "hints" like "in the original this is done such-and-such way", "the original function …".
- [ ] The unknown is not papered over with a guess: either `[?]`, or an item in `08_open_questions.md`.

## C. Release
- [ ] `check_spec.py` — no remarks.
- [ ] An entry in `spec/CHANGELOG.md`: release number, changed IDs, who reviewed, date.
- [ ] Answers to the questions in `spec/QUESTIONS.md` refer to rule IDs.
- [ ] The tag `spec-rN` is set, the archive is built with the command from `process/README.md`.
