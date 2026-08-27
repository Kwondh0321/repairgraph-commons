import json
import tempfile
import unittest
from pathlib import Path

from repairgraph.cli import main
from repairgraph.core import diagnose, validate_graph


def sample_graph():
    return {
        "nodes": [
            {
                "id": "symptom:no-power",
                "type": "symptom",
                "label": "will not power on",
                "aliases": ["no power"],
            },
            {"id": "cause:battery", "type": "cause", "label": "depleted battery"},
            {"id": "part:battery", "type": "part", "label": "replacement battery"},
            {
                "id": "procedure:replace",
                "type": "procedure",
                "label": "replace battery",
                "source": "https://example.org/repair",
            },
        ],
        "edges": [
            {
                "id": "e1",
                "from": "symptom:no-power",
                "to": "cause:battery",
                "type": "indicates",
                "confidence": 0.8,
            },
            {
                "id": "e2",
                "from": "cause:battery",
                "to": "part:battery",
                "type": "requires_part",
            },
            {
                "id": "e3",
                "from": "cause:battery",
                "to": "procedure:replace",
                "type": "resolved_by",
            },
        ],
    }


class RepairGraphTests(unittest.TestCase):
    def test_validates_and_queries_graph(self):
        graph = sample_graph()
        self.assertEqual([], validate_graph(graph))
        results = diagnose(graph, "device has no power")
        self.assertEqual("cause:battery", results[0]["cause"]["id"])
        self.assertEqual("part:battery", results[0]["parts"][0]["id"])

    def test_rejects_unknown_endpoints(self):
        graph = sample_graph()
        graph["edges"][0]["to"] = "missing"
        self.assertIn("RG008", {error["code"] for error in validate_graph(graph)})

    def test_cli_validate(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "graph.json"
            path.write_text(json.dumps(sample_graph()), encoding="utf-8")
            self.assertEqual(0, main(["validate", str(path)]))

    def test_rejects_invalid_optional_metadata_and_boolean_confidence(self):
        graph = sample_graph()
        graph["nodes"][0]["aliases"] = "no power"
        graph["edges"][0]["confidence"] = True
        codes = {error["code"] for error in validate_graph(graph)}
        self.assertIn("RG010", codes)
        self.assertIn("RG011", codes)


if __name__ == "__main__":
    unittest.main()
