"""Flask app serving the system report dashboard."""

from __future__ import annotations

import os

from flask import Flask, jsonify, render_template, request

from systemreports.collector import collect_report


def create_app() -> Flask:
    root = os.path.dirname(os.path.abspath(__file__))
    app = Flask(
        __name__,
        template_folder=os.path.join(root, "templates"),
        static_folder=os.path.join(root, "static"),
    )

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/api/report")
    def api_report():
        ports = request.args.get("ports", "1").lower() not in ("0", "false", "no")
        return jsonify(collect_report(include_listen_ports=ports))

    return app


def run_server(host: str = "127.0.0.1", port: int = 5050, debug: bool = False) -> None:
    app = create_app()
    app.run(host=host, port=port, debug=debug, threaded=True)
