#!/usr/bin/env python3
"""
Safe CPU monitor - read-only, non-admin.
Depends: psutil (pip install psutil)
"""
import argparse
import platform
import psutil
import shutil
import time
from datetime import datetime

AI_PROCESS_NAMES = {"python", "python3", "python.exe", "node", "node.exe", "java", "java.exe"}


def system_info():
    return {
        "platform": platform.system(),
        "platform_release": platform.release(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "cpu_count_logical": psutil.cpu_count(logical=True),
        "cpu_count_physical": psutil.cpu_count(logical=False),
    }


def cpu_stats(percpu=True):
    freq = psutil.cpu_freq()
    return {
        "total_load_percent": psutil.cpu_percent(interval=0.5),
        "current_frequency_mhz": round(freq.current) if freq else None,
        "per_core_percent": [round(p, 1) for p in psutil.cpu_percent(percpu=True, interval=0.5)],
    }


def memory_stats():
    vm = psutil.virtual_memory()
    return {
        "total_gb": round(vm.total / (1024 ** 3), 2),
        "used_gb": round((vm.total - vm.available) / (1024 ** 3), 2),
        "used_percent": vm.percent,
        "available_gb": round(vm.available / (1024 ** 3), 2),
    }


def estimate_power_watts(cpu_load_percent: float, tdp_watts: float = 65.0) -> float:
    # Simple heuristic: proportion of TDP scaled by utilization.
    # This is an estimate only — read-only, non-admin.
    scale = 0.75  # conservative multiplier for average power vs TDP
    return round((cpu_load_percent / 100.0) * tdp_watts * scale, 2)


def detect_ai_processes():
    procs = []
    for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
        try:
            name = (p.info.get("name") or "").lower()
            if name in AI_PROCESS_NAMES:
                # force a quick cpu_percent sample
                cpu = p.cpu_percent(interval=0.0)
                procs.append(
                    {"pid": p.info["pid"], "name": p.info["name"], "cpu_percent": round(cpu, 2),
                     "memory_percent": round(p.info.get("memory_percent", 0.0), 2)}
                )
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return procs


def print_header(title: str):
    width = shutil.get_terminal_size((80, 20)).columns
    print(title)
    print("=" * min(width, len(title) + 10))


def run_monitor(interval: float, duration: float, tdp: float):
    end = time.time() + duration if duration > 0 else None
    print_header("� Safe CPU Power Monitor Demo (READ-ONLY)")
    info = system_info()
    print("System Information")
    for k, v in info.items():
        print(f"  {k}: {v}")
    print()

    try:
        while True:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cs = cpu_stats()
            ms = memory_stats()
            ai = detect_ai_processes()
            est_power = estimate_power_watts(cs["total_load_percent"], tdp)

            print_header(f"📊 System Monitor - {now}")
            print(f"🔥 CPU Statistics:\n  Total Load: {cs['total_load_percent']}%\n  Frequency: {cs['current_frequency_mhz']} MHz")
            per_core = cs.get("per_core_percent") or []
            # shorten per-core list for compact display
            display_cores = per_core if len(per_core) <= 12 else per_core[:8] + ["..."] + per_core[-3:]
            print(f"  Per Core: {display_cores}\n")
            print(f"💾 Memory Statistics:\n  Total: {ms['total_gb']} GB\n  Used: {ms['used_gb']} GB ({ms['used_percent']}%)\n  Available: {ms['available_gb']} GB\n")
            print(f"⚡ Power Estimate:\n  Estimated (W): {est_power}W  (tdp={tdp}W heuristic)\n")
            if ai:
                print("🤖 AI Processes Detected:")
                for p in ai:
                    print(f"  {p['name']} (PID {p['pid']}): {p['cpu_percent']}% CPU, {p['memory_percent']}% MEM")
            else:
                print("🤖 AI Processes Detected: None")
            print()
            # stop condition
            if end and time.time() >= end:
                print("Monitor duration complete.")
                break
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nMonitor stopped by user.")


def parse_args():
    parser = argparse.ArgumentParser(description="Safe CPU monitor (read-only, non-admin).")
    parser.add_argument("--interval", type=float, default=5.0, help="Seconds between samples.")
    parser.add_argument("--duration", type=float, default=0.0, help="Total duration in seconds (0 = run until Ctrl+C).")
    parser.add_argument("--tdp", type=float, default=65.0, help="Nominal CPU TDP in watts for power estimation.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_monitor(interval=args.interval, duration=args.duration, tdp=args.tdp)
