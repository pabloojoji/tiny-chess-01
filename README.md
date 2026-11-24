[![make.fun](https://make.fun/badge.svg)](https://make.fun/bounty/tiny-chess-01)
[![make.fun](https://make.fun/badge2.svg)](https://make.fun/bounty/tiny-chess-01)
[![make.fun](https://make.fun/badge3.svg)](https://make.fun/bounty/tiny-chess-01)

# Tiny Chess — Fresh General Engine
Bounty: https://make.fun/bounty/tiny-chess-01
Entry for tiny-chess-01 by sgn88 (@sgn-8).

A 4,095-byte Python chess engine. PeSTO-style PSTs + alpha-beta with quiescence, transposition-free fixed-depth search, mate-distance-first, deterministic fixed node cap (20,000). No book, no practice-opening memorisation — a general engine, fresh for the unseen final openings.
Run: `python3 main.py` (prints best move in UCI, e.g. `b1c3`). Set `TEST_FEN` to test a position. Talks to `MAKEFUN_ENV_URL` via POST /game, /move, /resign.
