from pathlib import Path
import pandas as pd
import subprocess, tempfile

ALIASES = {
    "gyroADC[0]":"gyro_roll","gyroADC[1]":"gyro_pitch","gyroADC[2]":"gyro_yaw",
    "gyro[0]":"gyro_roll","gyro[1]":"gyro_pitch","gyro[2]":"gyro_yaw",
    "setpoint[0]":"setpoint_roll","setpoint[1]":"setpoint_pitch","setpoint[2]":"setpoint_yaw",
    "motor[0]":"motor_1","motor[1]":"motor_2","motor[2]":"motor_3","motor[3]":"motor_4",
}

def load_blackbox(path: str) -> pd.DataFrame:
    p = Path(path)
    suffix = p.suffix.lower()
    if suffix in [".csv",".tsv"]:
        df = pd.read_csv(p, sep="\t" if suffix == ".tsv" else ",")
    elif suffix in [".bbl",".bfl"]:
        try:
            data = subprocess.check_output(["blackbox_decode","--stdout",str(p)], text=True, errors="ignore", timeout=90)
        except Exception as e:
            raise RuntimeError("Install blackbox_decode/blackbox-tools or export CSV from Blackbox Explorer.") from e
        import io
        df = pd.read_csv(io.StringIO(data))
    else:
        raise ValueError("Unsupported log format")
    return df.rename(columns={c: ALIASES.get(c,c) for c in df.columns})
