# Exact fixed-IV S16 families and the first terminal A gate

## Result

The sealed fixed-IV `S16` merge is not isolated.  It belongs to an exact
Cartesian family of size

```text
2^15 selector choices * 2^32 W18 choices = 2^47.
```

Every member starts from the standard SHA-256 IV, forward-expands from its
sixteen initial words, satisfies the seven early equalities

```text
dA8 = dA9 = ... = dA14 = 0,
```

and therefore has equal complete states at `S16`.

A preregistered subset of 256 selector choices crossed with every `W18`
value was scanned completely.  This is exactly `2^40` members of the
family.  It contains 261 exact roots of the first terminal coordinate
`dA32=0`.  All 261 were reconstructed and scalar-replayed.  None also has
`dA33=0`, and none collides at `S40`.

This constructs the first terminal gate while preserving the fixed-IV early
merge.  It is not a 40-round collision and does not establish an improved
attack bound.

## The 15-bit selector family

At the boundary before round 14, put

```text
x = E11_left
p = dW7
epsilon10 = dE10.
```

The last selector equation is

```text
D_m(x,p) = -epsilon10,    m = ~E13.
```

For the sealed numerical core this gives the exact affine cube

```text
E13 & f7e10327 = 94400321
free mask          = 081efcd8
free bits          = 15.
```

Each `E13` reconstructs one common shift of the two `W13` words.  Complete
enumeration proves that all 32,768 values preserve the same weight-24
expanded support and the exact `S16` merge.  None passes `dA32=0` when the
original `W18` is retained.  The minimum total Hamming weight over
`dA32..dA39` is 97, at

```text
cube index = 26221
E13        = 9c529be9
W13        = 7ffee8c9.
```

The canonical census digest is

```text
d412bcda449578d9465a1e3d1f4d4b49e764742fb30d838fc04474e741f5d3f1.
```

## The 32-bit W18 family

Choose an arbitrary absolute left `W18`.  Since SHA-256 small sigma 1 is a
32-bit bijection, reconstruct

```text
W16 = sigma1^-1(W18 - W11 - sigma0(W3) - W2)
W14 = sigma1^-1(W16 - W9 - sigma0(W1) - W0).
```

`W14` is common to both messages.  Changing it does not change any of the
seven established `A` equalities: the first affected common state word moves
in both executions, and `dW15=-dW7` still cancels the sole delayed
disturbance.  Direct replay checks the complete `S16` equality.

Both inversions are bijective, so this is an exact `2^32` family, not a
sample.  Crossing it with the independent `E13` cube gives the `2^47`
Cartesian family.

Generic members activate the proposed `W20/W22` direction.  The 261 saved
first-gate roots all have exact support

```text
{7,8,10,11,13,15,18,20,22,23,24,25,26,27,28,29,30,31,
 32,33,34,35,36,37,38,39}.
```

Thus allowing `W20` and `W22` to differ removes the first-terminal-gate
obstruction found on the original fixed `W18` slice.  It does not control
the second terminal gate automatically.

## Complete searches

The original selector point was first crossed with all `2^32` `W18` values.
It has no `dA32` root.  Two distribution controls were recorded:

| Test | Exact count |
| --- | ---: |
| low 16 bits of `dA32` are zero | 65,612 |
| low 24 bits of `dA32` are zero | 239 |
| complete `dA32` zero | 0 |

The bounded Cartesian scan used the deterministic selector sequence

```text
cube_index(i) = (i * 0x4f1d + 0x1234) mod 2^15,
0 <= i < 256.
```

For every selected point, the full `2^32` `W18` axis was covered in sixteen
`2^28` chunks.  The aggregate results are:

| Quantity | Exact result |
| --- | ---: |
| Selector axes | 256 |
| Candidates per axis | `2^32` |
| Total candidates | `2^40` |
| low-16 zeros | 16,774,448 |
| low-24 zeros | 65,623 |
| `dA32=0` roots | 261 |
| `dA32=dA33=0` roots | 0 |
| `S40` collisions | 0 |

The aggregate checkpoint and root digest is

```text
efdc6482fdda65dc0a558a2b2261c4ec8c285f04181dcffdc86513c8f3ce2b4a.
```

The measured kernel time on the NVIDIA GeForce GTX 1070 Ti was about 380
seconds.  This is descriptive evidence for the finite census, not an attack
cost ledger.

## Exact terminal coordinates

For any fixed pair of `S32` states and fixed left words `W32..W39`, there is
one partner suffix that makes `A32..A39` equal in sequence.  Eight consecutive
`A` words are an invertible coordinate system for the SHA-256 state, so all
eight equalities are equivalent to equality at `S40`.

The packet records both views for every retained root:

* the actual modular differences `dA32..dA39`;
* the difference between the expanded right suffix and the unique required
  compensating suffix.

At an `A32` root the first value in both lists is zero.  Every retained root
has a nonzero second value.  The next exact construction target is therefore
`A33`, with `E12` or another independent coordinate released; extending the
same fixed two-coordinate census cannot change its complete negative result.

## Verification

`verify.py` is an independent scalar implementation.  It:

* derives the selector cube from the round equation;
* enumerates and replays all 32,768 selector members;
* verifies complete, nonoverlapping coverage of the base `W18` axis;
* recomputes the 256-axis checkpoint digest and aggregate counts;
* expands and compresses all 261 positive records from their initial words;
* confirms `S16`, `dA32`, exact support, nonzero `dA33`, and unequal `S40`.

`scan_w18.py --verify` additionally compares 4,096 OpenCL results field for
field with the scalar evaluator before accepting the GPU implementation.

The source witness reported `dW30=1215c42b`; this packet treats that as an
active schedule word.  It does not interpret the older partial row-30 core
identity as an assertion that the expanded `dW30` is zero.

## Evidence boundary

Established:

* an exact `2^15` fixed-IV `S16` selector family;
* an exact bijective `2^32` `W18 -> W16 -> W14` family;
* their exact `2^47` Cartesian product;
* complete coverage of a predetermined `2^40` subset;
* 261 independently replayed first-terminal-gate roots;
* zero second-gate roots and zero `S40` collisions in that subset.

Not established:

* complete coverage of the remaining `2^47 - 2^40` members;
* a construction satisfying `A32` and `A33` together;
* a terminal merge or 40-round SHA-256 collision;
* a success-probability model or improved Yukon/HashSmash cost.

Run `./RUN.sh` to verify the sealed files, replay every retained positive,
regenerate the complete selector census, and compare the OpenCL evaluator
with the scalar reference.
