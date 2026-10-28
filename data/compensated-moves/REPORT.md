# Cross-family compensating modifications

This packet screens exact changes to the actual pinned core words of Z10, Z01/Z1, Z00 and S7. It finds local schedule switches and compensators, then records their influence on the two compression trajectories. Local validity does not establish a composable group or an attack gain.

| Family / scope | Mode | Unique valid moves | All single atoms fail | Minimal compensators | Same full schedule difference at every tested point |
| --- | --- | ---: | ---: | ---: | ---: |
| Z10_core | fixed_initial_xor | 33 | 7 | 7 | 0 |
| Z10_core | literal_common_xor | 29 | 3 | 3 | 0 |
| Z10_core | literal_common_modular | 21 | 3 | 3 | 0 |
| Z01_Z1_core | fixed_initial_xor | 15 | 2 | 2 | 0 |
| Z01_Z1_core | literal_common_xor | 15 | 2 | 2 | 0 |
| Z01_Z1_core | literal_common_modular | 15 | 2 | 2 | 0 |
| third_Z00_core | fixed_initial_xor | 108 | 7 | 7 | unlifted |
| third_Z00_core | literal_common_xor | 82 | 5 | 5 | unlifted |
| third_Z00_core | literal_common_modular | 140 | 7 | 7 | unlifted |
| S7_core | fixed_initial_xor | 254 | 9 | 8 | 180 |
| S7_core | literal_common_xor | 242 | 7 | 7 | 180 |
| S7_core | literal_common_modular | 268 | 17 | 16 | 191 |
| third_Z00_direct_witness | fixed_initial_xor | 0 | 0 | 0 | 0 |
| third_Z00_direct_witness | literal_common_xor | 0 | 0 | 0 | 0 |
| third_Z00_direct_witness | literal_common_modular | 0 | 0 | 0 | 0 |

The core scope uses pins W4,W12,W13,W27 for Z10; W1,W6,W14,W15,W29 for Z01; W1,W3,W8,W16,W17,W31 for Z00; and W7,W8,W10,W15,W23,W24 for S7. All masks refer to those real schedule coordinates. The initial difference values and witness pairs are copied with SHA-256 provenance in data/INPUTS.json.

Z10, Z01 and S7 have verified acyclic charts. Their support closure certificates prove every reported core move has exact support for every coordinate choice. Every move also receives full schedule and state replay at four deterministic chart points. Z00 has a verified core and witness, but no verified chart here. Its formal-core rows are marked unlifted and carry no state claims. A separate three-word direct-input screen changes W1,W3,W8 on the saved Z00 witness and checks the actual 40-word expansions.

Three semantics are kept separate. fixed_initial_xor matches the older neutral-switch convention, changing the base pin and rebuilding the partner from fixed initial deltas. literal_common_xor changes both branch endpoints by the same XOR mask and verifies the induced modular deltas. literal_common_modular adds the same signed powers of two to both endpoints. The latter preserves every moved pin difference. All singleton, pair and triple subsets of these primitive atoms are exhausted; modular net identities are removed and duplicate resulting changes are deduplicated.

A compensator is a valid combined move whose individual atoms all fail the corresponding exact support/core test. A minimal compensator also has no valid nonempty proper subset. These definitions prevent pairs of already valid switches from being counted as compensating discoveries. Formal Z00 compensators solve only its core equations.

results/influence.jsonl contains one row per valid schedule transformation. Each row gives the first changed base and partner schedule word, the first changed absolute state, every invariant modular a-difference through S40, selected condition-bit preservation, full state-difference boundary preservation, dW38/dW39 changes and S39/S40 terminal changes. Schedule-difference-neutral, support-neutral with variable deltas, condition-wise compensation and invalid representatives remain separate.

The condition screen compares bits 0,7,15,23,31 of the modular a-difference at the listed early and terminal cuts with the same frozen chart point. It records combinations that restore a selected bit while every individual atom flips it. These conditions are finite diagnostics. No target differential characteristic is assumed, and the counts do not supply a chart-conditioned success probability.

Every valid move is composed with the same bounded set of up to 64 valid moves from its own family and semantics. A failed composition is an exact counterexample; passing those tests is labelled bounded evidence only. results/selected_spans.json exhausts the span of all discovered low-weight XOR moves, up to rank 20. Every family here fits that cap. It reports every invalid span point count, without claiming maximality beyond the explicitly screened ambient space.

Of the 8 selected XOR spans, 3 contain invalid combinations of individually valid generators. The saved composition counterexamples show the resulting actual support whenever a chart or direct witness is available.

Selected exact compensators at the first frozen chart point:

| Family / semantics | Net changes | First changed W, base / partner | First changed S, base / partner | Invariant modular a indices | dW38 changes |
| --- | --- | --- | --- | --- | --- |
| Z10 / fixed_initial_xor | W12=00001000, W27=00000020 | 0 / 0 | 1 / 1 | 0,1,2,3,4,5 | True |
| Z01_Z1 / fixed_initial_xor | W29=08000004 | 0 / 0 | 1 / 1 | 0,1,2 | True |
| S7 / fixed_initial_xor | W10=00800000, W23=00000010 | 10 / 10 | 11 / 11 | 0,1,2,3,4,5,6,7,8,9,10,11 | True |
| S7 / fixed_initial_xor | W10=00802000, W23=00000010 | 10 / 10 | 11 / 11 | 0,1,2,3,4,5,6,7,8,9,10,11 | True |
| S7 / fixed_initial_xor | W24=000000a0 | 12 / 12 | 13 / 13 | 0,1,2,3,4,5,6,7,8,9,10,11,12,13 | False |
| S7 / literal_common_modular | W10=00000080, W23=07fc0000 | 10 / 10 | 11 / 11 | 0,1,2,3,4,5,6,7,8,9,10,11 | True |

For S7, XOR W10 bit 23 together with W23 bit 4 is valid. XOR W10 bits 13 and 23 together with W23 bit 4 is also valid. Composing the two leaves only W10 bit 13, which is invalid. The first failed recurrence row is 25 and its exact modular residual is ffffff80. The fixed-initial S7 low-weight masks span rank 19; an exhaustive core check of that whole 524,288-point span rejects 131,072 points. This is the concrete reason to test a whole switch family.

The modular S7 triple in the table is +2^7 at W10, -2^18 and +2^27 at W23. All three individual atoms fail the exact core closure; the combination restores it. Z01 has two minimal fixed-initial XOR compensators in this search, both within one word. No cross-word irreducible Z01 compensator appears at weight at most three in the stated atom domain.

All accepted literal-common XOR moves in Z10, Z01 and S7 retain every initial modular difference in the searched domain. They supply no different-initial-delta variant. All common modular moves retain initial differences by construction.

No combined move restored a selected full modular a-difference boundary when every single atom changed that same full word. Selected individual condition bits do show such restorations. The JSON distinguishes cases in which all singleton schedules are themselves valid from cases in which singleton support already fails.

Run bash RUN.sh to compile and rerun all screens and replays, then verify SHA256SUMS. The rerun uses only this packet and a C++17 compiler plus Python 3 standard library. The imported arithmetic implementations are independently compared on every baseline point; every copied witness is checked against both exact schedule implementations. No root document is modified. No collision, probability, cost improvement or attack-bound claim follows from this screen.
