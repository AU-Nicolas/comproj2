from __future__ import annotations

from flask import Flask, render_template, request


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def dashboard():
        return render_template("dashboard.html")

    @app.get("/live")
    def live_status():
        return render_template("live_status.html")

    @app.get("/history")
    def visit_history():
        return render_template("visit_history.html")

    @app.get("/sensors")
    def sensors():
        return render_template("sensors.html")

    @app.get("/settings")
    def settings():
        return render_template("settings.html")

    @app.get("/search")
    def search():
        # Placeholder route: do not perform any real search logic yet.
        q = (request.args.get("q") or "").strip()
        return render_template("dashboard.html", search_query=q)

    return app


if __name__ == "__main__":
    create_app().run(debug=True, host="127.0.0.1", port=5000)
