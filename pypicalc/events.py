from keg.signals import app_ready


@app_ready.connect
def init_extensions(app):
    """Init custom extensions used by this application"""

    app.mail.init_app(app)
