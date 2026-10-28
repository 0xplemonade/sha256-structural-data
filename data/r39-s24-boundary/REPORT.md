# Boundary architecture for the two compensated r39 families

## Result

Both compensated weight-seven schedule families admit the same exact
semi-free-start boundary formulation. At a cut `S_c`, choose the left state
`X` and compare two right states:

```text
Jpre_c(X) = P_R,c(P_L,c^-1(X))
Jsuf_c(X) = Q_R,c^-1(Q_L,c(X)).
```

`P` maps the common CV through rounds `0..c-1`. `Q` maps the cut state
through rounds `c..37`. The pair is a 39-step semi-free-start collision if
and only if

```text
Jpre_c(X) = Jsuf_c(X).
```

The exact `S24` formulation is the smallest of the four tested cuts after
both schedules are constants. Its state-word equation has 24,406 shared
QF_BV DAG nodes for support `{6,7,9,14,22,23,37}` and 24,235 nodes for
support `{6,8,9,14,22,23,37}`. Direct inversion from a common `S38` has
40,927 and 40,954 nodes, respectively. The `S24` reduction is 40.37% and
40.82%.

This is a smaller exact representation. It is not evidence that the equation
has a solution or that a solver can invert it efficiently. Every output word
at every tested cut depends on all eight boundary words.

The packet also gives a precise negative result. For every cut and family,
all 127 nontrivial partitions of the eight boundary words fail both a global
componentwise modular-additive separator and a global componentwise XOR
separator. The 2,032 retained four-corner counterexamples use the complete
SHA-256 additions and carries.

No r39 collision was found.

## 1. The cut equation is exact

Fix one pair of 39-word expanded schedules. Let

```text
P_L,c : CV -> S_c,left
P_R,c : CV -> S_c,right
Q_L,c : S_c,left -> S38,left
Q_R,c : S_c,right -> S38,right.
```

Every SHA-256 round is bijective when its schedule word is fixed. The four
maps are therefore bijective. For a chosen left boundary state `X`, the
prefix relation forces the right boundary state

```text
Jpre_c(X) = P_R,c(P_L,c^-1(X)).
```

The left suffix reaches `Q_L,c(X)`. Requiring the right suffix to reach that
same state forces

```text
Jsuf_c(X) = Q_R,c^-1(Q_L,c(X)).
```

The two executions have one common CV and one common `S38` exactly when the
two forced right boundary states are equal. Because `W38` is common in both
families, equality at `S38` is also equality at `S39`.

The direct common-terminal formulation chooses a common `S38`, inverts both
complete prefixes, and equates the two recovered CVs. It has the same zero
set as every boundary equation. The independent verifier tested this
equivalence on 1,024 random boundary states.

## 2. Eight consecutive A words are exact coordinates

For a state `(a,b,c,d,e,f,g,h)`, define the four older A words:

```text
u3 = e - a + Sigma0(b) + Maj(b,c,d)
u2 = f - b + Sigma0(c) + Maj(c,d,u3)
u1 = g - c + Sigma0(d) + Maj(d,u3,u2)
u0 = h - d + Sigma0(u3) + Maj(u3,u2,u1).
```

Then

```text
(u0,u1,u2,u3,d,c,b,a)
```

is a bijective coordinate system for the state. Equality of the eight
coordinates is equivalent to equality of the eight state words.

This coordinate change does not simplify these fixed-schedule formulas. At
`S24`, it increases the DAG from 24,406 to 25,535 nodes for the first family
and from 24,235 to 25,364 nodes for the second. It also leaves every output
dependent on every boundary word.

## 3. `S24` gives the smallest tested fixed-schedule formula

The analyzer substitutes both complete schedules before it builds each
formula. It counts shared word-level QF_BV DAG nodes and records a canonical
DAG hash. It does not infer bit-blasted solver size from the word-level
count.

| Family | Formulation | DAG nodes | Maximum depth | Larger side at the cut |
| --- | --- | ---: | ---: | ---: |
| `{6,7,9,14,22,23,37}` | common `S38`, recover both CVs | 40,927 | 230 | n/a |
| same | `S8` | 30,028 | 315 | 29,812 |
| same | `S16` | 24,961 | 228 | 17,538 |
| same | `S24` | **24,406** | **184** | **17,238** |
| same | `S32` | 29,772 | 272 | 29,048 |
| `{6,8,9,14,22,23,37}` | common `S38`, recover both CVs | 40,954 | 230 | n/a |
| same | `S8` | 30,046 | 315 | 29,834 |
| same | `S16` | 24,800 | 228 | 17,534 |
| same | `S24` | **24,235** | **184** | **17,065** |
| same | `S32` | 29,631 | 272 | 28,906 |

`S24` is the best tested cut by total nodes, depth, and largest-side nodes.
The two families differ by less than 1% under every metric. The result
supports using `S24` for the next solver implementation. It does not show a
family-specific state advantage.

These counts cover one fixed schedule pair from each exact chart. A model
that restores the 320 chart bits, numerical-core variables, or derivative
root variables is a different formula.

## 4. Planted controls stay separate from zero targets

For each family and cut, the analyzer starts both prefixes from the standard
SHA-256 IV and records the left boundary state `X`. It computes the generally
nonzero residual `F(X)` and uses that value as a target-relaxed positive
control.

The analyzer then fixes every boundary bit except the low `1`, `2`, `4`, or
`8` bits of `X[0]`. It exhausts each fibre under both state-word and eight-A
coordinates. There are 64 declared fibres:

```text
2 families * 4 cuts * 2 coordinate forms * 4 hidden widths.
```

Every fibre has exactly one target-relaxed root, namely the planted member.
Every fibre has zero genuine zero-target roots. The widest fibres contain 256
states each. This proves only those finite exclusions.

Z3 received the 16 hidden-byte target-relaxed controls and the 16 matching
zero-target queries. All 32 queries returned `UNKNOWN` at 1.5 seconds. The
exhaustive enumerator still proves the root counts. The bounded `UNKNOWN`
results show that none of the tested representations recovers even the
one-byte planted controls under this budget.

## 5. Progressive zero-bit queries do not distinguish the cuts

The unbound boundary solver tested low `1`, `2`, `4`, and `8` bits of every
residual word under both coordinate forms. These are 64 partial zero-target
queries. It also tested 16 complete 256-bit zero targets.

All 80 queries returned `UNKNOWN` at 1.5 seconds. No model exists to replay.
The result is a solver observation, not a satisfiability result. In
particular, a low-bit `UNKNOWN` does not imply a low-bit obstruction.

## 6. A broad word-partition separator class is impossible

Let `F(X)` be the eight-word state residual at one cut. For each nontrivial
bipartition `A|B` of the eight input words, the packet tests two global forms:

```text
F(X_A,X_B) = L(X_A) + R(X_B) mod 2^32
F(X_A,X_B) = L(X_A) xor R(X_B).
```

There are 127 partitions after identifying a partition with its complement.
An additive separator must obey the four-corner identity

```text
F00 + F11 - F10 - F01 = 0 mod 2^32.
```

An XOR separator must obey

```text
F00 xor F11 xor F10 xor F01 = 0.
```

For both families and all four cuts, the analyzer retains a violating corner
for every partition and both operations. The independent scalar verifier
replayed all 2,032 counterexamples.

This excludes the declared global word-partition class. It does not exclude
bit-level separators, explicit carry-state separators, restricted
subfamilies, coordinate transforms, approximate decompositions, or
multi-stage meet-in-the-middle constructions.

## 7. Recommended next solver shape

Use the `S24` state-word equation as the fixed-schedule kernel. Add schedule
coordinates only after constant substitution and preprocessing have been
measured separately. The eight-A form adds structure that may help a custom
solver, but its direct QF_BV representation is larger and has the same word
dependencies.

Do not use a global additive or XOR split over boundary words. Any useful
split must expose smaller carry states, restrict the schedule family, or
change coordinates before the split.

## Evidence boundary

Established exactly:

- the cut-conjugacy theorem at `S8`, `S16`, `S24`, and `S32`;
- equivalence with common-terminal CV recovery;
- the eight-A state-coordinate bijection;
- fixed-schedule formula sizes and word dependency graphs;
- 64 complete hidden-bit fibres through width eight;
- no zero target in any of those finite fibres;
- exact refutation of all 127 word bipartitions for both declared separator
  operations, cuts, and families;
- independent scalar replay of both schedules, 1,024 cut identities, 4,448
  fibre values, and 2,032 separator counterexamples.

Not established:

- SAT or UNSAT for any full zero-target common-CV equation;
- a 39-step semi-free-start collision;
- a standard-IV or ordinary hash collision;
- a favorable differential characteristic;
- an attack success probability or cost improvement.

## Reproduction

Run the sealed replay:

```bash
cd r39_sfs_boundary_architecture
bash RUN.sh
```

To regenerate the bounded solver receipts and all metrics, run:

```bash
FULL=1 bash RUN.sh
```

Full regeneration takes several minutes and requires Python 3 and
`z3-solver`.

