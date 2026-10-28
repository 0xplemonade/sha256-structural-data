# Structural hypotheses from the combined SHA-256 evidence

## Bottom line

The combined evidence suggests a useful way to reorganize reduced-round
SHA-256 collision research:

```text
fixed-IV reset  ->  controlled reseed  ->  terminal repair
      S16                 W18               A32..A39
```

This is not a collision result. It is a construction hypothesis with exact
positive controls for its first and third components:

- a fixed-IV family of size `2^47` preserves complete equality at `S16`;
- a complete `2^40` census contains 261 exact `dA32=0` roots;
- no member of that census also has `dA33=0`.

The next question is therefore not whether another random `W18` slice contains
a two-word root. It is whether an additional state-dependent schedule
coordinate can preserve `S16` and `dA32` while constructing `dA33`.

The exact local findings and their evidence classes are recorded in
[`LEGACY_FINDINGS.json`](LEGACY_FINDINGS.json). The catalog binds 571
pre-Shaman artifacts in [`LEGACY_INDEX.json`](LEGACY_INDEX.json).

## What prior work already covers

Several ingredients are established and should not be claimed as new.

- Early SHA-256 attacks already use consecutive message words to control an
  internal state and reconnect a modified prefix to a semi-free-start
  characteristic. Mendel and coauthors explicitly describe control of the
  full state through consecutive words in
  [Collisions and Other Non-random Properties for Step-Reduced SHA-256](https://eprint.iacr.org/2008/131).
- The established SHA-2 method searches a message-expansion local collision,
  builds a signed state characteristic, applies message modification in its
  dense part, and spends probability in its sparse part. See
  [Improving Local Collisions](https://eprint.iacr.org/2015/350).
- AutoSHA2Collision automates local-collision discovery and improves the
  modeling of Boolean-function bit conditions. Its authors identify new local
  collisions in the message expansion as necessary for extending ordinary
  SHA-256 collision attacks beyond 31 steps. See
  [Collision Attacks on SHA-256 up to 37 Steps with Improved Trail Search](https://eprint.iacr.org/2026/232).
- Recent 38- and 39-step work uses an efficient meet-in-the-middle construction
  but still identifies a low-probability uncontrolled part as the barrier for
  39-step SHA-256. See
  [Pushing Collision Attacks on SHA-2 to 39 Steps](https://eprint.iacr.org/2026/1120).
- Programmatic SAT shows that SHA-specific deductions can change solver
  performance dramatically compared with generic SAT alone. See
  [SHA-256 Collision Attack with Programmatic SAT](https://arxiv.org/abs/2406.20072).
- Dual-syncopation tracks deterministic and nondeterministic information in
  two directions through ARX operations. Its successful SHA-256 applications
  are preimage attacks rather than the collision construction below. See
  [Dual-Syncopation Meet-in-the-Middle Attacks](https://eprint.iacr.org/2026/353).

The possible contribution is the exact combination below, not reversible
rounds, state-first coordinates, message modification, SAT, or meet-in-the-
middle search by themselves.

## Hypothesis 1: reset-reseed-repair is a useful decomposition

### Exact evidence

The fixed-IV diagonal-S7 branch supplies a complete state reset:

```text
S16_left = S16_right.
```

The two schedules remain common through `W17`; active `W18` then restarts the
state difference. The saved construction extends to an exact `2^47` family:
15 selector bits crossed with all 32 bits of absolute `W18`.

For a terminal state at `S40`, the eight consecutive produced words

```text
A32, A33, ..., A39
```

are exact state coordinates. A collision is therefore equivalent to eight
word equations `dA32=...=dA39=0`. For fixed states at the start of a terminal
round and a fixed left schedule word, exactly one right schedule word produces
the required next `A` equality. Thus the terminal repair words form an exact
graph over the two boundary states.

The ordinary message expansion forms a second graph. A 40-round collision is
an intersection of these two graphs inside the fixed-IV S16 family.

### Structural interpretation

The schedule has ample nominal freedom, but the freedom is usually transverse
to the terminal repair graph. The 261 `dA32` roots show that the first
codimension-32 intersection is nonempty. Zero joint `dA32,dA33` roots in the
declared `2^40` census is consistent with another independent 32-bit gate.

This does not prove independence. It tells us what a useful non-generic
structure must do: create a direction tangent to the `dA32=0` fibre while
moving `dA33` predictably.

### Falsifiable experiment

At all 261 saved `dA32` roots:

1. release one numerical-core or schedule coordinate that was fixed in the
   original `2^47` family;
2. enumerate or solve its complete exact root fibre under `S16` and
   `dA32=0`;
3. measure the induced exact `dA33` image, including carries;
4. search a second coordinate only after the first fibre is explicit;
5. replay every `dA33=0` result through all 40 rounds.

A complete fixed-IV `dA32=dA33=0` witness produced by a new repair rule would
be the first real advancement of this construction. It may be expensive.

## Hypothesis 2: valid schedule moves have curvature

The cross-family packet found exact combined moves for which every individual
atom violates schedule closure. It also found valid S7 moves whose composition
is invalid, with the first exact residual appearing at row 25.

Therefore, valid schedule modifications do not form a context-independent
linear space or group under the tested operations. A useful exact obstruction
for closure residual `C` is the second difference

```text
Omega_x(p,q) = C(x+p+q) - C(x+p) - C(x+q) + C(x).
```

The operations and subtraction domain must be declared explicitly. A nonzero
`Omega` records interaction that singleton neutral-bit models miss. A zero
closed loop can still move a later state residual.

This suggests searching short loops in a schedule fibre:

```text
disturb -> compensate schedule -> move state -> restore protected gates.
```

The loop, not an individual mask, is the search object. Auxiliary paths and
boomerang-style repairs are related ideas, but the exact closure residual and
state effect can be measured here for every step of the program.

## Hypothesis 3: carry states are the missing separator

For the r39 compensated supports, `S24` is the smallest tested exact boundary
formula. Every one of the 127 nontrivial word partitions fails both the global
modular-additive and XOR four-corner tests. The inside-out atlas likewise found
that each tested byte coordinate affected every boundary word.

These results refute word-level separation. They do not refute a separator
conditioned on a small set of addition carries.

The next representation should expose native carry variables inside the
actual adders, then eliminate local variables while retaining only:

```text
selected S24 bits + selected carry states + root identity.
```

Paul and Preneel proved that a restricted but important class of coupled
differential equations of addition admits polynomial-time satisfiability and
output-sensitive enumeration. See
[Solving Systems of Differential Equations of Addition](https://eprint.iacr.org/2004/294).
Raddum and Semaev's relation-joining method gives a second exact model for
combining sparse local solutions through shared variables. See
[New Technique for Solving Sparse Equation Systems](https://eprint.iacr.org/2006/475).

The hypothesis fails if conditioning on every small carry signature leaves the
same wide interface or causes intermediate relations to grow beyond the direct
SAT formula.

## Hypothesis 4: support search should include boundary rank

Z00, Z01, and Z10 are exact weight-seven class-Z schedule supports ending at
`W38`, with common `W39`. Z10 has an exact `2^384` chart. The P8 structure, by
contrast, has an exact obstruction at the next schedule word. These are
different tail classes even before state compatibility is considered.

Existing automated trail search optimizes local-collision and Boolean trail
quality. A combined search can rank a support by four exact properties:

1. schedule liftability and chart dimension;
2. the last active word and next-word defect;
3. fixed-IV reachability of a useful early boundary;
4. rank and carry structure of the terminal A-window map.

Large chart dimension alone is not a useful score. The relevant quantity is
freedom that survives inside the kernel of already constructed state gates.

## Highest-value combined construction

The most interesting experiment combines two previously separate lines:

1. start from the fixed-IV S16 reset family;
2. release coordinates that change the post-S16 support class;
3. solve for a Z10- or Z01-like common-tail geometry while preserving S16;
4. enforce `dA32=0` using the saved first-gate controls;
5. derive a carry-conditioned correction for `dA33`;
6. continue the terminal A window only after exact replay.

This would be a support-changing bridge between a state-compatible prefix and
a large exact tail chart. No reviewed public source above describes this exact
bridge, and exact-support web searches did not locate the saved Z01 or Z10
supports. That is evidence for a novelty audit, not proof of novelty.

## Claim boundary

Established by the local evidence:

- exact fixed-IV S16 reset and `2^47` family;
- 261 exact first-terminal-word roots in a complete declared `2^40` census;
- exact Z01 and Z10 schedule witnesses and Z10 chart;
- exact failure of every tested global S24 word partition;
- exact context dependence of several compensated schedule moves.

Not established:

- a two-word terminal root in the expanded S16 family;
- a complete r39 or r40 collision from these constructions;
- a small carry-conditioned separator;
- a probability or attack-cost improvement;
- formal novelty relative to all unpublished or unindexed work.

The immediate scientific target is one exact fixed-IV `S16 + dA32 + dA33`
witness constructed by a reusable rule. That result would justify continuing
the terminal window and would be meaningful even before its cost is
competitive.
