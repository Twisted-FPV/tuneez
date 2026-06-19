import numpy as np
from scipy import signal

def series(df, name):
    if name in df:
        arr = np.asarray(df[name].dropna(), dtype=float)
        return arr if len(arr) > 8 else np.array([])
    return np.array([])

def fs(df):
    for col in ["time","time_us","time (us)"]:
        if col in df:
            t = np.asarray(df[col].dropna(), dtype=float)
            if len(t) > 3:
                dt = np.median(np.diff(t))
                if dt > 100:
                    return 1_000_000.0 / dt
                if dt > 0:
                    return 1.0 / dt
    return 2000.0

def welch_peak(x, sample_rate):
    if len(x) < 64:
        return {"peak_hz":0.0,"noise_energy":0.0}
    f,p = signal.welch(x-np.mean(x), fs=sample_rate, nperseg=min(1024,len(x)))
    idx = int(np.argmax(p[1:])+1) if len(p)>1 else 0
    return {"peak_hz":float(f[idx]), "noise_energy":float(np.trapezoid(p,f))}

def tracking(setpoint, gyro):
    n = min(len(setpoint), len(gyro))
    if n < 16:
        return {"tracking_error":0.0,"overshoot_ratio":0.0}
    sp, gy = setpoint[:n], gyro[:n]
    active = np.abs(sp) > max(20.0, np.percentile(np.abs(sp), 65))
    if not active.any():
        active = np.ones(n, dtype=bool)
    err = np.mean(np.abs(sp[active]-gy[active]))
    over = np.maximum(np.abs(gy[active]) - np.abs(sp[active]), 0)
    return {"tracking_error":float(err), "overshoot_ratio":float(np.mean(over)/(np.mean(np.abs(sp[active]))+1e-6))}

def motors(df):
    cols=[c for c in df.columns if c.startswith("motor_")]
    if not cols:
        return {"saturation":0.0,"imbalance":0.0}
    arr=df[cols].to_numpy(dtype=float)
    high=np.nanmax(arr)
    sat=float(np.nanmean(arr > high*0.95)) if high else 0.0
    means=np.nanmean(arr,axis=0)
    return {"saturation":sat, "imbalance":float(np.nanstd(means)/(np.nanmean(means)+1e-6))}
