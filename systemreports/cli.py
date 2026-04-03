"""Command-line entry: web dashboard or legacy text report."""

from __future__ import annotations

import argparse
import json
import webbrowser


def _print_text_report() -> None:
    """Original-style console output using the new collector."""
    from systemreports.collector import collect_report

    r = collect_report(include_listen_ports=False)
    cpu = r["cpu"]
    mem = r["memory"]
    sysinfo = r["system"]
    disk = r["disk"]
    net = r["network"]
    up = r["uptime"]
    load = cpu["load_average"]
    load_s = (
        f"({load['1m']}, {load['5m']}, {load['15m']})" if load else "N/A (not available on this OS)"
    )
    print("This System Report is Generated on :-", r["generated_at"])
    print("=========================================================")
    print("Name of Operating System is      :- ", sysinfo["os"], sysinfo["release"])
    print("Host Name                        :- ", sysinfo["node"])
    print("Load Average                     :- ", load_s)
    print("System Architecture              :- ", sysinfo["machine"])
    print("Kernel / version detail          :- ", sysinfo["version"][:120])
    print("CPU model                        :- ", cpu["model"])
    print("CPU cores (physical / logical)   :- ", cpu["physical_cores"], "/", cpu["logical_cores"])
    print("CPU usage %                      :- ", cpu["usage_percent"])
    print("root Disk mount                  :- ", disk["mount"])
    print("Disk total / used / free (GB)    :- ", disk["total_gb"], "/", disk["used_gb"], "/", disk["free_gb"])
    print("Memory total / used / free (GB)  :- ", mem["total_gb"], "/", mem["used_gb"], "/", mem["free_gb"])
    print("Swap used (GB) / %               :- ", mem["swap_used_gb"], "/", mem["swap_percent"])
    print("Process count                    :- ", r["processes"]["count"])
    print("Uptime (seconds)                 :- ", up["seconds"])
    print("Last boot (local)                :- ", up["boot_time_iso"])
    print("Primary IPv4                     :- ", net["primary_ipv4"])
    print("DNS google.com                   :- ", net["dns_google_reachable"])


def main() -> None:
    p = argparse.ArgumentParser(description="System report: web dashboard or CLI output.")
    p.add_argument("--cli", action="store_true", help="Print text report to the console.")
    p.add_argument("--json", action="store_true", help="Print full JSON report to stdout.")
    p.add_argument("--host", default="127.0.0.1", help="Bind address for --serve.")
    p.add_argument("--port", type=int, default=5050, help="Port for --serve.")
    p.add_argument("--no-browser", action="store_true", help="Do not open a browser with --serve.")
    p.add_argument("--debug", action="store_true", help="Flask debug mode (dev only).")
    args = p.parse_args()

    if args.json:
        from systemreports.collector import collect_report

        print(json.dumps(collect_report(), indent=2))
        return

    if args.cli:
        _print_text_report()
        return

    # Default: web dashboard
    if not args.no_browser:
        url = f"http://{args.host}:{args.port}/"
        if args.host in ("0.0.0.0", "::"):
            url = f"http://127.0.0.1:{args.port}/"
        webbrowser.open(url)
    from systemreports.app import run_server

    run_server(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
