"""Validation and deterministic querying for repair knowledge graphs."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

NODE_TYPES = {"device", "symptom", "cause", "part", "procedure", "safety"}
EDGE_TYPES = {
    "has_symptom",
    "indicates",
    "requires_part",
    "resolved_by",
    "has_safety_note",
    "compatible_with",
}


def load_graph(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError("graph must be a JSON object")
    return value


def validate_graph(graph: dict[str, Any]) -> list[dict[str, str]]:
    """Return machine-readable validation errors."""
    errors: list[dict[str, str]] = []
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    if not isinstance(nodes, list) or not isinstance(edges, list):
        return [
            {
                "code": "RG001",
                "location": "$",
                "message": "nodes와 edges는 배열이어야 합니다.",
            }
        ]

    ids: set[str] = set()
    for index, node in enumerate(nodes):
        location = f"nodes[{index}]"
        if (
            not isinstance(node, dict)
            or not isinstance(node.get("id"), str)
            or not node.get("id", "").strip()
            or not isinstance(node.get("label"), str)
            or not node.get("label", "").strip()
        ):
            errors.append(
                {
                    "code": "RG002",
                    "location": location,
                    "message": "node에는 비어 있지 않은 문자열 id와 label이 필요합니다.",
                }
            )
            continue
        if node["id"] in ids:
            errors.append(
                {
                    "code": "RG003",
                    "location": location,
                    "message": f"node id가 중복됐습니다: {node['id']}",
                }
            )
        ids.add(node["id"])
        if node.get("type") not in NODE_TYPES:
            errors.append(
                {
                    "code": "RG004",
                    "location": location,
                    "message": f"지원하지 않는 node type입니다: {node.get('type')}",
                }
            )
        if node.get("type") == "procedure" and (
            not isinstance(node.get("source"), str) or not node["source"].strip()
        ):
            errors.append(
                {
                    "code": "RG005",
                    "location": location,
                    "message": "수리 절차에는 문자열 source URL 또는 인용이 필요합니다.",
                }
            )
        for key in ("aliases", "tags"):
            if key in node and (
                not isinstance(node[key], list)
                or not all(isinstance(value, str) for value in node[key])
            ):
                errors.append(
                    {
                        "code": "RG011",
                        "location": f"{location}.{key}",
                        "message": f"{key}는 문자열 배열이어야 합니다.",
                    }
                )

    edge_ids: set[str] = set()
    for index, edge in enumerate(edges):
        location = f"edges[{index}]"
        if not isinstance(edge, dict) or not all(
            isinstance(edge.get(key), str) for key in ("id", "from", "to", "type")
        ):
            errors.append(
                {
                    "code": "RG006",
                    "location": location,
                    "message": "edge에는 문자열 id, from, to, type이 필요합니다.",
                }
            )
            continue
        if edge["id"] in edge_ids:
            errors.append(
                {
                    "code": "RG007",
                    "location": location,
                    "message": f"edge id가 중복됐습니다: {edge['id']}",
                }
            )
        edge_ids.add(edge["id"])
        if edge["from"] not in ids or edge["to"] not in ids:
            errors.append(
                {
                    "code": "RG008",
                    "location": location,
                    "message": "edge가 존재하지 않는 node를 참조합니다.",
                }
            )
        if edge["type"] not in EDGE_TYPES:
            errors.append(
                {
                    "code": "RG009",
                    "location": location,
                    "message": f"지원하지 않는 edge type입니다: {edge['type']}",
                }
            )
        weight = edge.get("confidence", 1.0)
        if (
            isinstance(weight, bool)
            or not isinstance(weight, (int, float))
            or not 0 <= weight <= 1
        ):
            errors.append(
                {
                    "code": "RG010",
                    "location": location,
                    "message": "confidence는 0과 1 사이의 숫자여야 합니다.",
                }
            )
    return errors


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[\w가-힣]+", text.lower()))


def diagnose(graph: dict[str, Any], query: str, limit: int = 5) -> list[dict[str, Any]]:
    """Rank causes and attach repair evidence for a free-text symptom query."""
    errors = validate_graph(graph)
    if errors:
        raise ValueError(f"그래프에 검증 오류 {len(errors)}개가 있습니다.")
    nodes = {node["id"]: node for node in graph["nodes"]}
    outgoing: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for edge in graph["edges"]:
        outgoing[edge["from"]].append(edge)

    query_tokens = _tokens(query)
    matched_symptoms = []
    for node in nodes.values():
        if node["type"] != "symptom":
            continue
        node_tokens = _tokens(
            " ".join([node["label"], *node.get("aliases", []), *node.get("tags", [])])
        )
        overlap = len(query_tokens & node_tokens)
        if overlap:
            matched_symptoms.append((node, overlap / max(1, len(query_tokens))))

    cause_scores: dict[str, float] = defaultdict(float)
    evidence: dict[str, list[str]] = defaultdict(list)
    for symptom, match_score in matched_symptoms:
        for edge in outgoing[symptom["id"]]:
            target = nodes[edge["to"]]
            if edge["type"] == "indicates" and target["type"] == "cause":
                score = match_score * float(edge.get("confidence", 1.0))
                cause_scores[target["id"]] = max(cause_scores[target["id"]], score)
                evidence[target["id"]].append(symptom["label"])

    results = []
    for cause_id, score in sorted(
        cause_scores.items(), key=lambda item: (-item[1], nodes[item[0]]["label"])
    )[:limit]:
        repairs = []
        parts = []
        safety = []
        for edge in outgoing[cause_id]:
            target = nodes[edge["to"]]
            if edge["type"] == "resolved_by":
                repairs.append(target)
            elif edge["type"] == "requires_part":
                parts.append(target)
            elif edge["type"] == "has_safety_note":
                safety.append(target)
        results.append(
            {
                "cause": nodes[cause_id],
                "score": round(score, 4),
                "matched_symptoms": sorted(set(evidence[cause_id])),
                "repairs": repairs,
                "parts": parts,
                "safety": safety,
            }
        )
    return results
