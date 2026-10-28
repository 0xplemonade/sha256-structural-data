# Exact structural datasets for reduced-round SHA-256

This repository publishes compact, independently replayable data from a
proof-guided search for SHA-256 collision constructions. It is intended as
shared research material.

It does **not** contain a new collision, an improved attack exponent, or a
claim about full SHA-256.

## Included datasets

### Fixed-IV S16 family

`data/s16-fixed-iv/` contains:

- an exact pair of 40-word schedules whose states merge at `S16` from the
  standard SHA-256 IV;
- an exact `2^47` family preserving that merge;
- complete accounting for a declared `2^40` subset;
- 261 replayed roots of the first terminal equation `dA32=0`;
- zero roots of the joint `dA32=dA33=0` event in that subset.

The 261 roots include both initial message blocks and all eight terminal
`A`-word differences, so they can seed attempts to construct the second gate.

### Z00, Z01, and Z10 schedule families

`data/z-class-schedules/` contains exact schedule pairs on supports

```text
Z00  {1,3,8,16,17,31,38}
Z01  {1,6,14,15,29,36,38}
Z10  {4,12,13,27,34,36,38}
```

All three have common `W39`. Z10 includes an exact `2^384` schedule chart.
These are schedule constructions, not state collisions.

### r39 S24 boundary data

`data/r39-s24-boundary/` contains exact boundary metrics for the compensated
supports `{6,7,9,14,22,23,37}` and `{6,8,9,14,22,23,37}`. It also contains
2,032 concrete four-corner counterexamples refuting every global additive and
XOR partition of the eight boundary words at the tested cuts.

The counterexamples do not rule out bit-level or carry-conditioned joins.

### Compensated schedule moves

`data/compensated-moves/` contains exact Z10, Z01/Z1, and S7 transformations.
Some combined transformations are valid even though every atom fails alone.
Some individually valid S7 transformations compose into an invalid schedule,
with the first retained residual at row 25.

### r38 fixed-CV solver record

`data/r38-fixed-cv/` contains compact results from 144 complete fixed-CV
queries and 216 solver calls. Sixteen known-satisfiable free-CV controls and
eight first-block-derived CV cases all remained `UNKNOWN` under the hidden
recovery formulations. `UNKNOWN` is not `UNSAT`.

## Verification

Run:

```bash
python3 verify_release.py
```

The verifier uses only Python's standard library. It checks `MANIFEST.sha256`,
re-expands every Z witness, replays all 261 fixed-IV first-gate roots through
40 SHA-256 rounds, checks the r39 separator counts, and checks the stated r38
query boundary.

## Suggested research use

The highest-value open experiment is to preserve both `S16` equality and
`dA32=0` while constructing `dA33=0`. Another promising direction is a
carry-conditioned r39 `S24` relation join.

The broader structural synthesis is in
[`docs/STRUCTURAL_HYPOTHESES.md`](docs/STRUCTURAL_HYPOTHESES.md).

## Sources and scope

The public literature already covers state control through consecutive message
words, local-collision search, message modification, SAT guidance, and
meet-in-the-middle propagation. Relevant primary sources include:

- [Collisions and Other Non-random Properties for Step-Reduced SHA-256](https://eprint.iacr.org/2008/131)
- [Improving Local Collisions](https://eprint.iacr.org/2015/350)
- [Collision Attacks on SHA-256 up to 37 Steps with Improved Trail Search](https://eprint.iacr.org/2026/232)
- [Pushing Collision Attacks on SHA-2 to 39 Steps](https://eprint.iacr.org/2026/1120)
- [SHA-256 Collision Attack with Programmatic SAT](https://arxiv.org/abs/2406.20072)
- [Dual-Syncopation Meet-in-the-Middle Attacks](https://eprint.iacr.org/2026/353)

The possible contribution here is the exact combination of a fixed-IV reset,
a controlled disturbance restart, and terminal A-window construction. Formal
novelty has not been established.

## Integrity and privacy

- Every included file is listed in `MANIFEST.sha256`.
- The release excludes private worker state, model transcripts, API material,
  absolute workspace paths, solver dumps, binaries, and interrupted cycle 43.
- Empty results and negative finite experiments are retained with their exact
  scopes.

## License

Generated data and documentation are available under CC BY 4.0. The standalone
verifier is available under the MIT License. See `LICENSE`.
