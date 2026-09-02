"""Load and validate the local CB-Dock3 YAML configuration."""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - depends on the user's environment
    raise SystemExit(
        "Missing dependency: PyYAML. Install the repository requirements with "
        "`python -m pip install -r requirements.txt`."
    ) from exc


TOOL_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = TOOL_DIR.parents[1]
DEFAULT_CONFIG = TOOL_DIR / "configurations" / "config.yaml"


def load_config(path: str | Path | None = None) -> dict[str, Any]:
    """Return the CB-Dock config after checking fields used by the scripts."""
    config_path = Path(path).resolve() if path else DEFAULT_CONFIG

    with config_path.open(encoding="utf-8") as handle:
        config = yaml.safe_load(handle) or {}

    # Keep tool-specific values grouped under the template's existing `extra`
    # key while exposing them consistently to the helper scripts.
    for key, value in (config.get("extra") or {}).items():
        config.setdefault(key, value)

    required = {
        "tool",
        "tool_slug",
        "branch",
        "software_version",
        "targets",
        "score_direction",
        "score_unit",
        "mode",
        "box",
        "pocket_detection",
        "number_of_cavities",
        "scoring_function",
        "selection_rule",
    }
    missing = sorted(required - config.keys())
    if missing:
        raise ValueError(
            f"Missing required key(s) in {config_path}: {', '.join(missing)}"
        )

    if config["score_direction"] not in {
        "lower_is_better",
        "higher_is_better",
    }:
        raise ValueError(
            "score_direction must be lower_is_better or higher_is_better"
        )

    if not isinstance(config["targets"], list) or not config["targets"]:
        raise ValueError("targets must be a non-empty list")

    if not isinstance(config["number_of_cavities"], int):
        raise ValueError("number_of_cavities must be an integer")

    return config


def result_docking_parameters(config: dict[str, Any]) -> dict[str, Any]:
    """Select the configuration fields stored in DOCKING_RESULT.json."""
    keys = (
        "mode",
        "box",
        "pocket_detection",
        "number_of_cavities",
        "scoring_function",
        "exhaustiveness",
        "num_poses",
        "random_seed",
        "selection_rule",
        "template_results_used",
    )
    return {key: config.get(key) for key in keys}
