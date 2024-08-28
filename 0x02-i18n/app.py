#!/usr/bin/env python3
"""Flask app with Babel, user locale preference,
and time zone selection
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, _, format_datetime
import pytz
from pytz.exceptions import UnknownTimeZoneError
from datetime import datetime


class Config:
    """Configuration class for Babel"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)


babel = Babel(app)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """Retrieve user information based on the login_as parameter"""
    try:
        user_id = int(request.args.get('login_as'))
        return users.get(user_id)
    except (TypeError, ValueError):
        return None


@babel.localeselector
def get_locale():
    """Determine the best match for supported languages"""
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale

    user = g.get('user')
    if user and user.get('locale') in app.config['LANGUAGES']:
        return user.get('locale')

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    """Determine the best time zone"""
    timezone = request.args.get('timezone')
    if timezone:
        try:
            pytz.timezone(timezone)
            return timezone
        except UnknownTimeZoneError:
            pass

    user = g.get('user')
    if user:
        timezone = user.get('timezone')
        if timezone:
            try:
                pytz.timezone(timezone)
                return timezone
            except UnknownTimeZoneError:
                pass

    return app.config['BABEL_DEFAULT_TIMEZONE']


@app.before_request
def before_request():
    """Executed before all other functions, to check if a user is logged in"""
    g.user = get_user()


@app.route('/')
def index():
    """Route for the index page"""
    timezone = get_timezone()
    current_time = datetime.now(pytz.timezone(timezone))
    formatted_time = format_datetime(current_time)
    return render_template('index.html', current_time=formatted_time)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
