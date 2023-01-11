"""
Timeblock: Flask app for task management & calendar scheduling.

To run the app, run the following command in the terminal:

    $ python -m timeblock

The app will be available at http://localhost:5000.

Please note that Timeblock is currently a work-in-progress.
"""


from flask import Flask

from timeblock.views import ROUTES


def main(database="db.sql"):
    """Run the Timeblock app."""
    app = Flask(__name__)
    app.register_blueprint(ROUTES)
    app.config["DATABASE"] = database
    app.run()
