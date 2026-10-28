#!/usr/bin/env python3
"""Independent standard-library verification for the public data release.

SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MASK = 0xFFFFFFFF
IV = (
    0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
    0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19,
)
K = (
    0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5,
    0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5,
    0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3,
    0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174,
    0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC,
    0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
    0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7,
    0xC6E00BF3, 0xD5A79147, 0x06CA6351, 0x14292967,
    0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13,
    0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85,
)


def load(path: str) -> object:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def rotate_right(value: int, count: int) -> int:
    return ((value >> count) | (value << (32 - count))) & MASK


def small0(value: int) -> int:
    return rotate_right(value, 7) ^ rotate_right(value, 18) ^ (value >> 3)


def small1(value: int) -> int:
    return rotate_right(value, 17) ^ rotate_right(value, 19) ^ (value >> 10)


def big0(value: int) -> int:
    return rotate_right(value, 2) ^ rotate_right(value, 13) ^ rotate_right(value, 22)


def big1(value: int) -> int:
    return rotate_right(value, 6) ^ rotate_right(value, 11) ^ rotate_right(value, 25)


def choose(x: int, y: int, z: int) -> int:
    return ((x & y) ^ ((~x) & z)) & MASK


def majority(x: int, y: int, z: int) -> int:
    return ((x & y) ^ (x & z) ^ (y & z)) & MASK


def expand(initial: tuple[int, ...]) -> tuple[int, ...]:
    assert len(initial) == 16
    words = list(initial)
    for index in range(16, 40):
        words.append((small1(words[index - 2]) + words[index - 7]
                      + small0(words[index - 15]) + words[index - 16]) & MASK)
    return tuple(words)


def run(words: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    states = [IV]
    for index, word in enumerate(words):
        a, b, c, d, e, f, g, h = states[-1]
        t1 = (h + big1(e) + choose(e, f, g) + K[index] + word) & MASK
        t2 = (big0(a) + majority(a, b, c)) & MASK
        states.append(((t1 + t2) & MASK, a, b, c, (d + t1) & MASK, e, f, g))
    return tuple(states)


def words(values: list[str]) -> tuple[int, ...]:
    return tuple(int(value, 16) for value in values)


def verify_manifest() -> int:
    manifest = ROOT / "MANIFEST.sha256"
    count = 0
    for line in manifest.read_text(encoding="ascii").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        assert match is not None
        expected, name = match.groups()
        relative = Path(name)
        assert not relative.is_absolute() and ".." not in relative.parts
        path = (ROOT / relative).resolve(strict=True)
        assert ROOT in path.parents and path.is_file()
        assert sha256(path) == expected, name
        count += 1
    return count


def verify_s16() -> int:
    scan = load("data/s16-fixed-iv/CUBE_AXIS_SCAN.json")
    roots = scan["roots"]
    assert scan["total_candidates"] == 1 << 40
    assert scan["first_gate_root_count"] == len(roots) == 261
    assert all(json.loads(path.read_text())["root_count"] >= 0
               for path in (ROOT / "data/s16-fixed-iv/cube_axis_checkpoints").glob("*.json"))
    assert len(list((ROOT / "data/s16-fixed-iv/cube_axis_checkpoints").glob("*.json"))) == 256
    for record in roots:
        left = expand(words(record["left_initial"]))
        right = expand(words(record["right_initial"]))
        left_states = run(left)
        right_states = run(right)
        assert left_states[16] == right_states[16]
        differences = tuple((right[index] - left[index]) & MASK for index in range(40))
        assert tuple(index for index, value in enumerate(differences) if value) == tuple(record["support"])
        terminal = tuple((right_states[index + 1][0] - left_states[index + 1][0]) & MASK
                         for index in range(32, 40))
        assert terminal == words(record["terminal_A_deltas"])
        assert terminal[0] == 0 and terminal[1] != 0
        assert left_states[40] != right_states[40] and record["S40_equal"] is False
    return len(roots)


def verify_z_witnesses() -> int:
    expected = {
        "Z00": (1, 3, 8, 16, 17, 31, 38),
        "Z01": (1, 6, 14, 15, 29, 36, 38),
        "Z10": (4, 12, 13, 27, 34, 36, 38),
    }
    for name, support in expected.items():
        record = load(f"data/z-class-schedules/results/{name}_witness.json")
        left = words(record["base_schedule"])
        right = words(record["partner_schedule"])
        assert expand(left[:16]) == left and expand(right[:16]) == right
        difference = tuple((b - a) & MASK for a, b in zip(left, right))
        assert tuple(index for index, value in enumerate(difference) if value) == support
        assert difference[39] == 0
    return len(expected)


def verify_s24_and_compensators() -> tuple[int, int]:
    separators = load("data/r39-s24-boundary/results/SEPARATOR_REFUTATIONS.json")
    cuts = 0
    for family in separators["families"].values():
        for result in family.values():
            assert result["additive_partitions_refuted"] == 127
            assert result["xor_partitions_refuted"] == 127
            assert len(result["evidence"]) == 127
            cuts += 1
    examples = load("data/compensated-moves/results/selected_examples.json")
    assert len(examples["examples"]) == 6
    assert examples["explicit_S7_nonclosure"]["first_failed_recurrence_row"] == {
        "difference": "ffffff80", "row": 25, "valid": False}
    return cuts, len(examples["examples"])


def verify_r38_boundary() -> int:
    summary = load("data/r38-fixed-cv/RESULTS/summary.json")
    assert summary["hidden_terminal_known_sat_cases"] == 16
    assert summary["hidden_terminal_cases_recovered"] == 0
    assert summary["sampled_fixed_iv_cases"] == 8
    assert summary["complete_search_queries"] == 144
    assert summary["ordinary_collision"] is None
    return summary["complete_search_queries"]


def main() -> None:
    s24_cuts, compensator_examples = verify_s24_and_compensators()
    result = {
        "manifest_files": verify_manifest(),
        "s16_roots_replayed": verify_s16(),
        "z_witnesses_replayed": verify_z_witnesses(),
        "s24_cuts_checked": s24_cuts,
        "compensator_examples_checked": compensator_examples,
        "r38_queries_recorded": verify_r38_boundary(),
        "collision_claim": False,
        "status": "PASS",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
