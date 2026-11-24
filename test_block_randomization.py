import unittest

from block_randomization import assign_next_subject


def run(n, sex, seed=12345):
    records = []
    for _ in range(n):
        g, s, _num = assign_next_subject(sex, records, seed=seed)
        records.append({"sex": sex, "group": g, "subgroup": s})
    return records


class TestBlockRandomization(unittest.TestCase):
    def test_reproducible(self):
        self.assertEqual(run(20, "F"), run(20, "F"))

    def test_balanced_every_four(self):
        records = run(40, "M")
        for g in "CS":
            for s in "12":
                n = sum(1 for r in records if (r["group"], r["subgroup"]) == (g, s))
                self.assertEqual(n, 10)

    def test_strata_independent(self):
        records = run(8, "F") + run(8, "M")
        _, _, n = assign_next_subject("F", records)
        self.assertEqual(n, 9)

    def test_unknown_cell_raises(self):
        with self.assertRaises(ValueError):
            assign_next_subject("F", [{"sex": "F", "group": "X", "subgroup": "1"}])


if __name__ == "__main__":
    unittest.main()
