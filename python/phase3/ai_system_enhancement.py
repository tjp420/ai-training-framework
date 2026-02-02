import json
import os
from typing import Dict

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), "ai_system_enhancement.json")

def load_config(path: str = None) -> Dict:
    path = path or DEFAULT_PATH
    with open(path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    if "components" not in cfg or "tasks" not in cfg:
        raise ValueError("Invalid config: missing 'components' or 'tasks'")
    weights = [v.get("weight", 0) for v in cfg["components"].values()]
    s = sum(weights)
    expected = cfg.get("validation", {}).get("weights_sum_expected", 1.0)
    if abs(s - expected) > 1e-2:
        raise ValueError(f"Component weights sum to {s:.6f}, expected ~{expected}")
    return cfg

if __name__ == "__main__":
    cfg = load_config()
    print("Loaded:", cfg.get("name"))
    print("Weights sum:", sum(v.get("weight",0) for v in cfg["components"].values()))
    print("Tasks:", len(cfg["tasks"]))
