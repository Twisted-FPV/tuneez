from .models import BuildProfile, Finding, TuneReport
from .cli_parser import get_num
from . import dsp

def analyze(df, cfg, build: BuildProfile) -> TuneReport:
    sample_rate = dsp.fs(df)
    findings = []
    scores = {
        "tracking": 82.0,
        "noise_health": 80.0,
        "thermal_safety": 80.0,
        "filter_efficiency": 76.0,
        "propwash_resistance": 75.0,
    }
    cli = []

    for axis in ["roll","pitch","yaw"]:
        sp = dsp.series(df, f"setpoint_{axis}")
        gy = dsp.series(df, f"gyro_{axis}")
        if len(sp) and len(gy):
            m = dsp.tracking(sp, gy)
            scores["tracking"] = max(0, scores["tracking"] - min(30, m["tracking_error"]/15))
            if m["overshoot_ratio"] > 0.10:
                p = get_num(cfg, f"p_{axis}", 50)
                cli.append(f"set p_{axis} = {max(1, round(p * 0.96))}")
                findings.append(Finding(
                    title=f"{axis.title()} overshoot",
                    severity="medium",
                    confidence=min(0.95, 0.58 + m["overshoot_ratio"]),
                    evidence=m,
                    why="The gyro exceeds the requested setpoint, which can feel like bounceback or a twitchy stop.",
                    recommendation=f"Reduce {axis} P slightly, or add damping only if motors are cool.",
                    risk="medium",
                ))

    for axis in ["roll","pitch"]:
        gy = dsp.series(df, f"gyro_{axis}")
        pk = dsp.welch_peak(gy, sample_rate)
        if pk["noise_energy"] > 1000 or pk["peak_hz"] > 120:
            scores["noise_health"] = max(0, scores["noise_health"] - 16)
            findings.append(Finding(
                title=f"{axis.title()} resonance/noise peak",
                severity="medium",
                confidence=0.72,
                evidence=pk,
                why="A strong gyro frequency peak can leak into D-term and heat motors or create oscillation.",
                recommendation="Keep RPM filtering enabled, inspect props/motors/frame, and avoid removing filters until the build is cleaner.",
                risk="medium",
            ))
            cli += ["set dyn_notch_count = 1", "set gyro_lpf1_dyn_min_hz = 80"]

    mot = dsp.motors(df)
    if mot["saturation"] > 0.08:
        scores["propwash_resistance"] = max(0, scores["propwash_resistance"] - 22)
        findings.append(Finding(
            title="Motor saturation risk",
            severity="high",
            confidence=0.80,
            evidence=mot,
            why="Motor outputs are reaching the top of available authority, reducing the FC's ability to correct attitude.",
            recommendation="Check AUW/props and consider tuning dynamic idle. Reduce aggressive P/FF if saturation happens during reversals.",
            risk="high",
        ))

    if mot["imbalance"] > 0.12:
        findings.append(Finding(
            title="Motor imbalance",
            severity="medium",
            confidence=0.70,
            evidence=mot,
            why="Uneven average motor work often points to CG imbalance, bent prop, twisted frame, or a weak motor.",
            recommendation="Inspect mechanics before chasing PID changes.",
            risk="medium",
        ))

    symptoms = [s.lower() for s in build.symptoms]
    if "hot motors" in symptoms:
        d = get_num(cfg, "d_pitch", 40)
        cli.append(f"set d_pitch = {max(1, round(d * 0.92))}")
        scores["thermal_safety"] = max(0, scores["thermal_safety"] - 25)
        findings.append(Finding(
            title="Hot motors symptom",
            severity="high",
            confidence=0.76,
            evidence={"symptom":"hot motors"},
            why="Hot motors commonly come from too much D gain, noisy D-term, weak filtering, or mechanical vibration.",
            recommendation="Reduce D slightly, inspect mechanical noise, and re-log after a short hover test.",
            risk="high",
        ))

    if (build.gyro or "").upper() == "BMI270":
        cli.append("set gyro_lpf1_dyn_min_hz = 70")
        findings.append(Finding(
            title="BMI270 conservative filter margin",
            severity="info",
            confidence=0.64,
            evidence={"gyro": build.gyro},
            why="BMI270 builds commonly benefit from more conservative gyro filtering than very clean MPU6000 builds.",
            recommendation="Keep filter changes conservative until logs prove the build is clean.",
            risk="low",
        ))

    if not findings:
        findings.append(Finding(
            title="No major issue detected",
            severity="info",
            confidence=0.55,
            evidence={},
            why="The available log columns did not show a high-confidence PID/filter fault.",
            recommendation="Collect another log with hover, cruise, flips, descents, and throttle chops for better diagnosis.",
            risk="low",
        ))
    if not cli:
        cli.append("# No high-confidence PID/filter CLI changes from this log.")
    cli.append("save")
    return TuneReport(
        scores=scores,
        findings=findings,
        cli="\n".join(dict.fromkeys(cli)),
        summary=f"Analyzed {len(df)} rows at estimated {sample_rate:.0f} Hz with {len(findings)} findings."
    )
