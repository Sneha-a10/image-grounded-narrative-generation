from typing import Dict, Any
import json
import os

# ==============================
# Module-Level Constants
# ==============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REGISTRY_PATH = os.path.join(BASE_DIR, "preset_registry.json")

def generate_constraints(
    request_payload: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Deterministic constraint generation entry point.
    """

    # Step 1 — Validate input
    _validate_input(request_payload)

    experiment_mode = request_payload["experiment_mode"]
    retry_count = request_payload["retry_count"]
    failure_type = request_payload["failure_type"]

    # Step 2 — Load registry
    registry = _load_registry()

    # Step 3 — Derive MAX_LEVEL
    max_level = _derive_max_level(registry, experiment_mode)

    # Step 4 — Select preset or hard reject
    selection_result = _select_preset(
        request_payload,
        registry,
        max_level
    )

    # HARD_REJECT path
    if selection_result.get("decision") == "HARD_REJECT":
        return selection_result

    # OK path
    preset = selection_result["preset"]
    preset_family = selection_result["preset_family"]
    preset_level = selection_result["preset_level"]

    constraints = _construct_constraint_object(preset)

    control_metadata = _construct_control_metadata(
        preset_family,
        preset_level,
        failure_type,
        max_level
    )

    return {
        "constraints": constraints,
        "control_metadata": control_metadata
    }

def _load_registry() -> Dict[str, Any]:
    """Load preset registry (deterministic read-only)."""

    if not os.path.exists(REGISTRY_PATH):
        raise FileNotFoundError(
            f"Preset registry not found at path: {REGISTRY_PATH}"
        )

    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        registry = json.load(f)

    if not isinstance(registry, dict):
        raise ValueError("Preset registry must be a dictionary.")

    return registry


def _validate_input(request_payload: Dict[str, Any]) -> None:
    """Validate request structure against interface contract."""

    if not isinstance(request_payload, dict):
        raise ValueError("Input must be a dictionary.")

    allowed_keys = {"experiment_mode", "retry_count", "failure_type"}

    if set(request_payload.keys()) != allowed_keys:
        raise ValueError("Invalid input structure.")

    experiment_mode = request_payload["experiment_mode"]
    retry_count = request_payload["retry_count"]
    failure_type = request_payload["failure_type"]

    if not isinstance(experiment_mode, str):
        raise ValueError("experiment_mode must be a string.")

    if not isinstance(retry_count, int) or retry_count < 0:
        raise ValueError("retry_count must be a non-negative integer.")

    if failure_type not in (None, "text", "image", "both"):
        raise ValueError("Invalid failure_type.")

def _derive_max_level(
    registry: Dict[str, Any],
    preset_family: str
) -> int:
    """Derive MAX_LEVEL from registry deterministically."""

    if preset_family not in registry:
        raise ValueError("Invalid preset family.")

    family_data = registry[preset_family]

    if "levels" not in family_data:
        raise ValueError("Preset family missing levels definition.")

    levels = family_data["levels"]

    if not isinstance(levels, dict) or not levels:
        raise ValueError("Levels must be a non-empty dictionary.")

    try:
        level_numbers = [int(level) for level in levels.keys()]
    except ValueError:
        raise ValueError("Level keys must be integers.")

    return max(level_numbers)

def _select_preset(
    request_payload: Dict[str, Any],
    registry: Dict[str, Any],
    max_level: int
) -> Dict[str, Any]:
    """Select preset using deterministic escalation logic."""

    experiment_mode = request_payload["experiment_mode"]
    retry_count = request_payload["retry_count"]
    failure_type = request_payload["failure_type"]

    if experiment_mode not in registry:
        raise ValueError("Invalid preset family.")

    if retry_count > max_level:
        return {
            "decision": "HARD_REJECT",
            "control_metadata": {
                "preset_family": experiment_mode,
                "preset_level": max_level,
                "trigger_reason": _map_trigger_reason(failure_type)
            }
        }

    family_levels = registry[experiment_mode]["levels"]

    if str(retry_count) not in family_levels:
        raise ValueError("Preset level not defined in registry.")

    return {
        "decision": "OK",
        "preset_family": experiment_mode,
        "preset_level": retry_count,
        "preset": family_levels[str(retry_count)]
    }

def _map_trigger_reason(failure_type: Any) -> str:
    if failure_type is None:
        return "initial"
    if failure_type == "text":
        return "text_failure"
    if failure_type == "image":
        return "image_failure"
    if failure_type == "both":
        return "both"
    raise ValueError("Invalid failure_type.")

def _emit_hard_reject(reason: str) -> Dict[str, Any]:
    """Emit hard reject structure per schema."""
    raise NotImplementedError


def _construct_constraint_object(
    preset: Dict[str, Any]
) -> Dict[str, Any]:
    """Build constraint object per schema."""

    required_fields = {
        "max_length",
        "tone",
        "perspective",
        "allowed_emotion_inference",
        "negative_rules"
    }

    if set(preset.keys()) != required_fields:
        raise ValueError("Preset schema mismatch.")

    max_length = preset["max_length"]
    tone = preset["tone"]
    perspective = preset["perspective"]
    allowed_emotion_inference = preset["allowed_emotion_inference"]
    negative_rules = preset["negative_rules"]

    if not isinstance(max_length, int) or max_length <= 0:
        raise ValueError("Invalid max_length.")

    if perspective != "third_person":
        raise ValueError("Perspective must be third_person.")

    if allowed_emotion_inference not in ("none", "limited"):
        raise ValueError("Invalid allowed_emotion_inference.")

    if not isinstance(negative_rules, list):
        raise ValueError("negative_rules must be a list.")

    if len(set(negative_rules)) != len(negative_rules):
        raise ValueError("Duplicate negative rules detected.")

    allowed_rules = {
        "NO_NEW_ENTITIES",
        "NO_INTERNAL_THOUGHTS",
        "NO_OFF_IMAGE_LOCATIONS",
        "NO_TEMPORAL_JUMPS",
        "NO_REFLECTIVE_LANGUAGE",
        "NO_ADJECTIVAL_EXPANSION",
        "NO_EXTENDED_METAPHOR"
    }

    for rule in negative_rules:
        if rule not in allowed_rules:
            # TEMP FIX — skip unsupported rules
            continue

    return {
        "max_length": max_length,
        "tone": tone,
        "perspective": perspective,
        "allowed_emotion_inference": allowed_emotion_inference,
        "negative_rules": list(negative_rules) 
    }

def _construct_control_metadata(
    preset_family: str,
    preset_level: int,
    failure_type: Any,
    max_level: int
) -> Dict[str, Any]:
    """Build control metadata per schema."""

    if not isinstance(preset_family, str):
        raise ValueError("Invalid preset_family.")

    if not isinstance(preset_level, int):
        raise ValueError("Invalid preset_level.")

    if preset_level < 0 or preset_level > max_level:
        raise ValueError("preset_level out of valid range.")

    trigger_reason = _map_trigger_reason(failure_type)

    return {
        "preset_family": preset_family,
        "preset_level": preset_level,
        "trigger_reason": trigger_reason
    }