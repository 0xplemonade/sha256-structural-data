The full fixed-CV W21 terminal relation is implemented and sealed. All 16 hidden terminal known-SAT controls and all eight sampled fixed-IV-derived CVs return UNKNOWN in every tested formulation. There are 144 complete queries and 216 solver calls. No hidden terminal control was recovered. No sampled fixed-IV terminal pair was found, and no UNSAT result was obtained. These budgets do not establish a working recovery method.

The packet binds `r38_common_suffix_codesign/SHA256SUMS` with SHA-256 `3abfe7bf4896d25a8967d14d6044bded21f628792ef934e00b3ccb25c600ae03`, the sealed relational solver, genuine panel, row17 audit, and audited P1 source commit `336054115d1f125633465be5c21b24e3aecb2092`. Copied payloads are checked against the retained input manifests. Every retained input has a provenance digest.

For a literal supplied CV, only 32-bit `a0`, 32-bit `u`, and a four-bit target tag are principal. The domain includes every `a0` in the hexadecimal R9 window `[24000000,28000000)` and every 32-bit `u`. A hidden control fixes its target tag; a sampled CV allows all 16 tags. Each tag selects its own exact row16 target and row17 parameters.

The early P1 equations reconstruct `a1=u-h(CV,a0)` and both complete 16-word blocks from the CV, a0, a1 and literal shifted core. Every word from W16 onward comes from the SHA-256 recurrence. In particular,

```text
W21 = sigma1(W19) + W14 + sigma0(W6) + W5   modulo 2^32
```

W21 is never a released variable in the fixed-CV search. Selecting it independently would change the problem. The relation requires the exact target-tagged P1 claw equation, all four original postfilters, the row17 carry automaton, and every original signed and cross-bit predicate in rows 16 through 21. The four postfilters are the W8 difference `fbc00800`, then sigma0 differences at W9, W8 and W7 of `043ff800`, `fe808000` and `03bff800`.

The full BV formulation expands both schedules through W37, computes both states through S38, and requires `DeltaW25=20000000`, `DeltaA18..24=0`, common W26..37 and equal S38. It uses the complete schedules induced by the early coordinates.

The reduced relation replaces the deep common suffix with

```text
sigma1(W23x + fe808000) - sigma1(W23x) = 4fffa0d0
sigma1(W25x + 20000000) - sigma1(W25x) = 0007f400
DeltaA17 + DeltaW25 = 0
DeltaA18 = ... = DeltaA24 = 0
```

The two imported universal schedule obligations are rechecked as UNSAT. The prefix/postfilters supply their first three residuals, and independent numeric checks bind all 16 exact W16 targets to the W17/W18 cancellation hypotheses. A new universal state obligation proves that the remaining `DeltaA17+DeltaW25` residual is exactly the S26 merge condition once A18..24 are common. Equal suffix words then preserve equality through S38. The full and reduced encodings also pass all coordinate-bound positive calibrations.

A further BV variant uses the separator worker's universal state lemmas. Original row21 already implies A22 equality. With that branch, A23 and A24 equality reduce to `E22x[29]=0` and `E23x[29]=1`. All four supplied universal obligations are independently rerun as UNSAT. The solver still computes the exact E22 and E23 values. It does not select their bits independently.

| Formulation | Fixed budget per case | Hidden terminal controls | Sampled fixed-IV cases |
| --- | --- | --- | --- |
| Full QF_BV | 1,000,000 Z3 units | 16 UNKNOWN | 8 UNKNOWN |
| Reduced schedule/state BV | 1,000,000 Z3 units | 16 UNKNOWN | 8 UNKNOWN |
| Reduced schedule/two-state-bit BV | 1,000,000 Z3 units | 16 UNKNOWN | 8 UNKNOWN |
| Carry CNF | 2,000 CryptoMiniSat conflicts | 16 UNKNOWN | 8 UNKNOWN |
| Carry XOR | 2,000 CryptoMiniSat conflicts | 16 UNKNOWN | 8 UNKNOWN |
| Progressive BV | 200k, 200k, 200k, 400k Z3 units | 16 UNKNOWN | 8 UNKNOWN |

Every query uses seed zero, one solver thread and a 30-second wall-clock backstop. The progressive solver adds low8 and low16 row16 equalities, the full schedule conditions, then the complete relation. It never binds a coordinate from an earlier partial model. All four stages were attempted for each case. Formula files, circuit variable maps, assigned budgets, statuses, unknown reasons and observed Z3 resource counts are retained. Z3 units and solver conflicts have no common cost conversion, so this is not a speed ranking.

The hidden benchmark contains only CV, tag/target and a coordinate commitment. Search does not read control messages or bind a0, u, W2, W21 or any early state. The 16 terminal controls are the sealed semi-free-start pairs, with retention repaired when required. Original tags2,5 and12 were overwritten. For these tags, W6=1 and a newly solved W21 give a retained terminal pair. Merely varying W6 while holding W21 fixed can break the merge because W22 changes; the initial calibration caught and rejected that mistake. All repaired controls pass complete schedules, literal predicates and S38 equality.

There are 80 coordinate-bound SAT calibrations across full BV, both reduced BV variants, CNF and XOR. Every extracted model is independently replayed. They prove encoding consistency and provide arithmetic-plus-table positive controls. They do not count as hidden recovery or as sampled fixed-IV successes. The verifier separately checks all 16 controls against a complete R9 last-writer scan.

Last-writer retention remains an exact external acceptance condition. A complete arithmetic SAT model must replay both full terminal blocks, pass every predicate, and survive all 2^26 R9 insertions at its `F>>6` address with a non-sentinel packed entry. BV can block an overwritten a0 and continue within the remaining original budget. The Python CryptoMiniSat binding does not expose remaining conflicts, so an overwritten CNF/XOR model would become UNKNOWN. No canonical query reached arithmetic SAT. The arithmetic formulas therefore are a compact relation plus an exact acceptance procedure; they do not pretend to contain a quantified table relation.

The independent verifier imports no producer relation or circuit arithmetic. It reconstructs the complete blocks using a separate eight-register implementation, expands both schedules, checks the original literal cells and cross-bit conditions, and verifies terminal state equality. It regenerates the eight genuine panel first blocks and their 38-round feed-forward CVs from the standard SHA-256 IV. Six universal early-coordinate identities and seven universal reduction obligations pass as UNSAT.

`VERIFY/scoped_root_counts.json` preserves the separator worker's tag-specific inverse-tail counts, ranging from 428 to 2487 terminal W21 values. These are counts within fixed per-control charts for W7..W20 and early state coordinates. They are not a complete W21 domain for arbitrary fixed-CV a0/u queries and are not used to restrict that search.

`RESULTS/ledger.json` records 96,000,000 assigned canonical Z3 units and 96,000 assigned canonical CryptoMiniSat conflicts, with calibration, universal proofs and terminal-control repair separate. Canonical preparation and independent retention verification perform 35 complete table scans, totaling 2,348,810,240 insertions. A narrow conservative scalar-RAM bound is supplied for the native table replay body only. Solver work has no audited word-RAM mapping. Charged computation per genuine terminal candidate, attack cost, attack memory, tail probability and score remain null. The canonical accepted-candidate denominator is zero.

The standard-IV first blocks are verified, and the 16 terminal pairs under their free CVs are verified. No terminal pair is verified under any sampled first-block CV. There is no ordinary fixed-IV collision claim.

Run `bash RUN.sh` to verify the seal and regenerate the complete packet in a temporary directory, including hidden searches. Every deterministic result, formula and verification byte is compared with the seal. `bash VERIFY.sh` runs the independent checks and bound calibrations without repeating hidden recovery. Both require Python 3.12, z3-solver, pycryptosat and g++. Observed timing files are diagnostics. The runner never invokes `code/seal.py`.
