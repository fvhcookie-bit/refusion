# ReFusion — behaviour specification of Wipeout Fusion

Русская версия: [README.ru.md](README.ru.md)

A description of the behaviour of **Wipeout Fusion** (PS2, PAL SCES-50005), written for an independent
clean-room implementation: rules with identifiers, formulas, constants, game file formats, test cases.

The repository **does not contain** game data (models, textures, sound, texts), the game's executable code,
disassembly or decompilation results. An implementation works with files that the user takes from their own copy of the game.
The project is not affiliated with the rights holders of the game; the names belong to their owners.

| folder | contents |
|---|---|
| [`docs/spec/`](docs/spec/README.md) | behaviour specification: rules with IDs, evidence labels, open questions, change log |
| [`docs/process/`](docs/process/README.md) | clean-room protocol, review checklist, `check_spec.py` |
| `docs/ru/` | Russian version of the documents in `docs/spec/` and `docs/process/` (the script `check_spec.py` is shared and lives only in `docs/process/`) |

Checking the specification for contamination: `python docs/process/check_spec.py`.
