# RepairGraph Commons

RepairGraph Commons defines and validates an open symptom–cause–part–procedure knowledge graph, then provides a deterministic query engine for repair tools. The repository separates reusable code from openly licensed graph data.

## Run

```bash
python -m pip install -e .
repairgraph validate data/example.graph.json
repairgraph query data/example.graph.json "laptop not charging"
```

## Graph model

Node types: `device`, `symptom`, `cause`, `part`, `procedure`, `safety`.

Edge types: `has_symptom`, `indicates`, `requires_part`, `resolved_by`, `has_safety_note`, `compatible_with`.

Every procedure requires a source citation. Edges may include a confidence from 0 to 1. Validation rejects duplicate IDs, missing endpoints, unknown types, invalid confidence values, and unsourced procedures.

Diagnostic rankings are suggestions from contributed graph relationships, not professional repair or electrical-safety advice. Always surface safety nodes and verify device-specific service documentation.

## Contributing data

Add small, source-backed graph changes with tests. Do not copy proprietary service manuals or submit uncertain compatibility claims. Code is MIT licensed; example graph data under `data/` is CC-BY-4.0.
