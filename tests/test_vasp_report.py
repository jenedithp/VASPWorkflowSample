import tempfile
import unittest
from pathlib import Path

from tools.vasp_report import parse_outcar


class VaspReportTests(unittest.TestCase):
    def test_sample_output_is_converged(self):
        report = parse_outcar(Path("examples/sample_OUTCAR"))

        self.assertTrue(report["converged"])
        self.assertEqual(report["ionic_steps"], 2)
        self.assertEqual(report["final_energy_ev"], -10.14567890)

    def test_missing_energy_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            outcar = Path(directory) / "OUTCAR"
            outcar.write_text("VASP output without energies", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "No final"):
                parse_outcar(outcar)


if __name__ == "__main__":
    unittest.main()
