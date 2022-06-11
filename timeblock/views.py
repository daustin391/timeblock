""" Views
    Handle display of interface for Timeblock app
"""
from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def index():
    """Main app view"""
    context = {"actions": [{"desc": "make coffee"}]}
    return render_template("actions.html", **context)


def runserver():
    """Runs Flask server"""
    app.run()


if __name__ == "__main__":
    runserver()
