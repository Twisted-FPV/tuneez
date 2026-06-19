import re
from typing import Dict
SET_RE = re.compile(r"^set\s+([a-zA-Z0-9_]+)\s*=\s*(.+?)\s*$")

def parse_cli_dump(text: str) -> Dict[str, str]:
    cfg = {}
    for line in text.splitlines():
        line=line.strip()
        if not line:
            continue
        if line.startswith("#"):
            if "Betaflight" in line or "INAV" in line:
                cfg["firmware_banner"] = line
            continue
        m = SET_RE.match(line)
        if m:
            cfg[m.group(1)] = m.group(2)
    return cfg

def get_num(cfg: Dict[str,str], key: str, default: float=0.0) -> float:
    try:
        return float(str(cfg.get(key, default)).split()[0])
    except Exception:
        return default
