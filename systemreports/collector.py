"""Gather system metrics on Windows, macOS, and Linux."""

from __future__ import annotations

import os
import platform
import socket
import sys
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import psutil


def _root_fs_path() -> str:
    if os.name == "nt":
        drive = os.environ.get("SystemDrive", "C:")
        return drive + (os.sep if not drive.endswith(("\\", "/")) else "")
    return "/"


def _bytes_to_gb(n: float) -> float:
    return round(n / (1024**3), 2)


def _bytes_to_mb(n: float) -> float:
    return round(n / (1024**2), 2)


def _safe_iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")


def _cpu_model() -> str:
    proc = platform.processor() or ""
    if proc.strip():
        return proc.strip()
    if sys.platform == "darwin":
        try:
            import subprocess

            out = subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"])
            return out.decode("utf-8", errors="ignore").strip()
        except (OSError, subprocess.CalledProcessError):
            pass
    if sys.platform.startswith("linux"):
        try:
            with open("/proc/cpuinfo", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if line.lower().startswith("model name"):
                        return line.split(":", 1)[1].strip()
        except OSError:
            pass
    return "Unknown"


def _load_average() -> Optional[Dict[str, float]]:
    try:
        one, five, fifteen = os.getloadavg()
        return {"1m": round(one, 2), "5m": round(five, 2), "15m": round(fifteen, 2)}
    except (AttributeError, OSError):
        return None


def _disk_io() -> Optional[Dict[str, Any]]:
    try:
        io = psutil.disk_io_counters(perdisk=False)
        if io is None:
            return None
        return {
            "read_bytes": io.read_bytes,
            "write_bytes": io.write_bytes,
            "read_count": io.read_count,
            "write_count": io.write_count,
        }
    except (RuntimeError, PermissionError):
        return None


def _network_interfaces() -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    addrs = psutil.net_if_addrs()
    stats = psutil.net_if_stats()
    for name, addr_list in addrs.items():
        entry: Dict[str, Any] = {"name": name, "addresses": [], "is_up": None, "speed_mbps": None}
        st = stats.get(name)
        if st:
            entry["is_up"] = st.isup
            entry["speed_mbps"] = st.speed if st.speed > 0 else None
        for a in addr_list:
            if a.family == socket.AF_INET:
                entry["addresses"].append({"family": "IPv4", "address": a.address, "netmask": a.netmask})
            elif a.family == socket.AF_INET6:
                entry["addresses"].append({"family": "IPv6", "address": a.address, "netmask": a.netmask})
            elif hasattr(psutil, "AF_LINK") and a.family == psutil.AF_LINK:
                entry["addresses"].append({"family": "MAC", "address": a.address})
        out.append(entry)
    return sorted(out, key=lambda x: x["name"])


def _primary_ipv4() -> Optional[str]:
    try:
        return socket.gethostbyname(socket.gethostname())
    except OSError:
        pass
    for iface in _network_interfaces():
        for a in iface["addresses"]:
            if a.get("family") == "IPv4" and not a["address"].startswith("127."):
                return a["address"]
    return None


def _listen_ports(limit: int = 80) -> Dict[str, Any]:
    try:
        conns = psutil.net_connections(kind="inet")
        ports = sorted(
            {c.laddr.port for c in conns if c.status == psutil.CONN_LISTEN and c.laddr}
        )
        return {"available": True, "ports": ports[:limit], "truncated": len(ports) > limit}
    except (psutil.AccessDenied, PermissionError):
        return {
            "available": False,
            "ports": [],
            "message": "Elevated permissions required to list listening ports on this OS.",
        }


def _top_processes_cpu(n: int = 8) -> List[Dict[str, Any]]:
    for p in psutil.process_iter(["pid", "name"]):
        try:
            p.cpu_percent(interval=None)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    time.sleep(0.15)
    procs: List[Dict[str, Any]] = []
    for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
        try:
            cpu = p.cpu_percent(interval=None)
            mem = p.memory_percent()
            rss = p.memory_info().rss
            procs.append(
                {
                    "pid": p.pid,
                    "name": p.info.get("name") or "?",
                    "cpu_percent": round(cpu or 0.0, 1),
                    "memory_percent": round(mem or 0.0, 1),
                    "rss_bytes": rss,
                    "rss_mb": _bytes_to_mb(rss),
                }
            )
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    procs.sort(key=lambda x: x["cpu_percent"], reverse=True)
    return procs[:n]


def _top_processes_memory(n: int = 8) -> List[Dict[str, Any]]:
    procs: List[Dict[str, Any]] = []
    for p in psutil.process_iter(["pid", "name"]):
        try:
            rss = p.memory_info().rss
            procs.append(
                {
                    "pid": p.pid,
                    "name": p.info.get("name") or "?",
                    "rss_bytes": rss,
                    "rss_mb": _bytes_to_mb(rss),
                    "memory_percent": round(p.memory_percent() or 0.0, 1),
                }
            )
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    procs.sort(key=lambda x: x["rss_bytes"], reverse=True)
    return procs[:n]


def collect_report(*, include_listen_ports: bool = True) -> Dict[str, Any]:
    """Return a JSON-serializable system report."""
    root = _root_fs_path()
    uname = platform.uname()
    boot = psutil.boot_time()
    vm = psutil.virtual_memory()
    sw = psutil.swap_memory()
    disk = psutil.disk_usage(root)
    phys = psutil.cpu_count(logical=False)
    logical = psutil.cpu_count(logical=True)
    cpu_pct = psutil.cpu_percent(interval=0.2)

    net_io = psutil.net_io_counters(pernic=False)
    net_totals = None
    if net_io:
        net_totals = {
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv,
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv,
        }

    report: Dict[str, Any] = {
        "generated_at": datetime.now().astimezone().isoformat(),
        "cpu": {
            "model": _cpu_model(),
            "physical_cores": phys,
            "logical_cores": logical,
            "usage_percent": round(cpu_pct, 1),
            "load_average": _load_average(),
        },
        "memory": {
            "total_bytes": vm.total,
            "total_gb": _bytes_to_gb(vm.total),
            "used_bytes": vm.used,
            "used_gb": _bytes_to_gb(vm.used),
            "free_bytes": vm.available,
            "free_gb": _bytes_to_gb(vm.available),
            "percent_used": round(vm.percent, 1),
            "swap_total_bytes": sw.total,
            "swap_total_gb": _bytes_to_gb(sw.total) if sw.total else 0,
            "swap_used_bytes": sw.used,
            "swap_used_gb": _bytes_to_gb(sw.used) if sw.used else 0,
            "swap_percent": round(sw.percent, 1) if sw.total else 0,
        },
        "system": {
            "os": uname.system,
            "node": uname.node,
            "release": uname.release,
            "version": uname.version,
            "machine": uname.machine,
            "platform": platform.platform(),
            "python_version": sys.version.split()[0],
        },
        "disk": {
            "mount": root,
            "total_bytes": disk.total,
            "total_gb": _bytes_to_gb(disk.total),
            "used_bytes": disk.used,
            "used_gb": _bytes_to_gb(disk.used),
            "free_bytes": disk.free,
            "free_gb": _bytes_to_gb(disk.free),
            "percent_used": round(disk.percent, 1),
            "io": _disk_io(),
        },
        "network": {
            "primary_ipv4": _primary_ipv4(),
            "interfaces": _network_interfaces(),
            "totals": net_totals,
            "dns_google_reachable": None,
        },
        "processes": {
            "count": len(psutil.pids()),
            "top_cpu": _top_processes_cpu(8),
            "top_memory": _top_processes_memory(8),
        },
        "uptime": {
            "seconds": int(time.time() - boot),
            "boot_time_iso": _safe_iso(boot),
        },
    }

    try:
        report["network"]["dns_google_reachable"] = socket.gethostbyname("google.com")
    except OSError:
        report["network"]["dns_google_reachable"] = None

    if include_listen_ports:
        report["network"]["listen_ports"] = _listen_ports()

    return report
