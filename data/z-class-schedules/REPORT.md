# Exact class-Z schedule hunt for 40-round SHA-256

## Result

All three previously untested weight-7 class-Z supports whose last active word
is `W38` have explicit, machine-replayed schedule pairs:

```text
Z00  {1,3,8,16,17,31,38}
Z01  {1,6,14,15,29,36,38}
Z10  {4,12,13,27,34,36,38}
```

For every pair, both 40-word schedules are genuine expansions of the saved
sixteen input words, every listed additive difference is nonzero, every word
outside the support is equal, and `dW39=0`.  These are the first exact positive
schedule results among the three highest-priority class-Z shapes.

This is a schedule result.  None of the saved points collides in compression
state, and no fixed-IV message collision, success probability, work bound, or
score is claimed.

## Complete support enumeration

The fourteen supports were reproduced independently from the frozen catalogue.
For every `t=16..39`, the exact partner-minus-base equation is

```text
d_t = D1(W_(t-2),d_(t-2)) + d_(t-7)
    + D0(W_(t-15),d_(t-15)) + d_(t-16)  mod 2^32,
```

where `Dj(W,d)=sigma_j(W+d)-sigma_j(W)`.  `systems.json` records every
nontrivial row and every nonzero requirement.  All fourteen are class Z:
`{23,24,32,37,39}` is inactive, hence `dW39=0` automatically.

An exact two-expansion CNF was generated for every support.  The three W38
families are SAT through reduced nonlinear cores plus absolute-base lifts.  A
two-second uniform screen left the other eleven **UNKNOWN**; none is labeled
UNSAT from a timeout.

| Status | Count |
| --- | ---: |
| SAT with integer-replayed schedule witness | 3 |
| UNSAT | 0 |
| UNKNOWN at the bounded screen | 11 |

## The three W38 witnesses

### Z00

```text
support {1,3,8,16,17,31,38}
d1  = 53c8f60d   d3  = 975f6a58   d8  = ac3709f3
d16 = 655b5c5d   d17 = 53c8f60d   d31 = d38 = 227488e5
```

The reduced core uses seven words and 4,171 Boolean variables.  It solves in
about 4.6 seconds.  Its absolute lift fixes `W1,W3,W8,W16,W17,W31`; the
14,360-variable lift solves in about 7.2 seconds.

The special top-bit chamber `d1=80000000` is UNSAT.  This obstruction is
isolated in the 2-adic hierarchy: valuation 31 has only that one nonzero
element, while both members of valuation 30, `40000000` and `c0000000`, are
SAT and independently replayed.  The full unpinned support is SAT at the value
above.

### Z01

```text
support {1,6,14,15,29,36,38}
d1  = 4ab4118d   d6  = df16d61f
d14 = 18a8ef9a   d15 = 20e929e1
d29 = d36 = ace5ce51   d38 = b0ea025e
```

The 3,648-variable reduced core solves in about four seconds.  Its absolute
lift solves in under one second.

### Z10

```text
support {4,12,13,27,34,36,38}
d4  = 01079e22   d12 = 2354dd23   d13 = fef861de
d27 = d34 = 7968b299   d36 = 1132700d   d38 = 95fb8eff
```

The 2,265-variable reduced core and its absolute lift both solve in under one
second.  `Z10_witness.json` contains the complete schedules.

`verify_w38.py` independently expands all six input blocks and verifies the
three exact supports and `dW39=0` without importing the solver encodings.

## Exact Z10 family

Z10 admits a residual-free `2^384` chart for the fixed nonlinear core.  Use the
consecutive schedule window `W5..W20`:

1. choose the twelve words `W5..W10,W14..W19` freely;
2. fix `W12,W13` to the core witness;
3. derive

   ```text
   W20 = W4 + sigma1(W18) + W13 + sigma0(W5);
   ```

4. expand `W21..W25`;
5. derive

   ```text
   W11 = W27 - sigma1(W25) - W20 - sigma0(W12);
   ```

6. reverse rows 20 through 16 to obtain `W4..W0`.

The twelve selected words remain visible in the schedule, so the chart is
injective.  Conversely every schedule in the fixed-core lift fibre has one
such window, so it is surjective for that core.  The exact family size is
therefore `2^(12*32)=2^384`.

The early differences `dW4,dW12,dW13,dW27,dW34` are fixed.  `dW36,dW38`
vary with the base schedule.  An exhaustive low-16-bit slice of coordinate
`W5`, with the other eleven coordinates zero, gives 65,536 distinct
`(dW36,dW38)` pairs.  Thus the late-delta family has an exact verified lower
bound of `2^16` distinct members; no claim that this is the global count is
made.

Because `W39` is common, equality after 40 rounds is equivalent to equality at
`S39`.  Pulling the active `W38` round back once gives the state-facing target

```text
at S38: delta a..g = 0,  delta h = -dW38.
```

`z10_family.py` exposes this exact residual for every chart coordinate.  On a
frozen 4,096-point sample, all `(dW36,dW38)` pairs were distinct, no state root
was found, and the `S39` difference weight ranged from 102 to 154 with mean
127.9602.  These are diagnostics, not a root probability.

## Z00 and Z01 family status

Both supports have nonempty absolute lift fibres, but no equally simple
residual-free chart was proved.  For Z00, the fixed `W31` word depends
structurally on all sixteen initial words after the `W16,W17` pins are
absorbed.  For Z01 the fixed `W29` word likewise depends on all sixteen input
words.  The expected dimension from equation counting is not reported as an
exact free-bit count.  Their family dimensions remain UNKNOWN, while their
saved points remain exact witnesses.

This is why Z10 is the primary state-facing family: its exact 384-bit chart is
available without a residual equation.

## State results and limits

The three fixed witnesses are dense under the standard IV:

| Witness | Maximum boundary weight | S38 terminal-residual weight | S39 equal? |
| --- | ---: | ---: | --- |
| Z00 | 142 | 112 | no |
| Z01 | 140 | 132 | no |
| Z10 | 138 | 108 | no |

For the concrete Z10 early cluster, two independent SAT backends report UNSAT:

- even from an arbitrary common `S4` with free inactive words, rounds 4..13
  cannot return the branches to equality at `S14`; and
- the same local-collision target is UNSAT from the fixed-IV prefix.

This is witness-specific and local.  A full collision need not become equal at
`S14`; a globally coupled early and late characteristic remains open.  The
result does show that the natural strategy “cancel the early cluster, then
cancel the late cluster” cannot use this Z10 core.

No conditional-affine Ch/Maj constraints were added to the schedule CNFs;
those belong in a future state formula after schedule feasibility, which is
now established.

## Reproduction

- `derive_systems.py` regenerates all fourteen modular systems.
- `support_cnf.py` builds the complete schedule formulas.
- `w38_cores.py` and `z10_core.py` build the reduced nonlinear cores.
- `lift_w38.py` and `lift_z10.py` produce genuine schedule witnesses.
- `z10_family.py` constructs and samples the exact `2^384` family.
- `verify_w38.py` and `verify_z10.py` provide independent integer replay.
- `campaign.py` records the bounded status of every open class-Z support.

The class-C extension was not attempted because the priority class-Z work
produced three schedule witnesses and the remaining work was used to freeze
and characterize the exact Z10 family.  No candidate, Yukon submission,
network service, or remote state was modified.
