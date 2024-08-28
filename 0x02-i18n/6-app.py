#!/usr/bin/env python3
"""Flask app with Babel, forced locale,
mock user login, and user locale preference
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, _


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
    """Determine the best match for
    supported languages with the following priority:
    1. Locale from URL parameters
    2. Locale from user settings
    3. Locale from request header
    4. Default locale
    """
    # 1. Locale from URL parameters
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale

    # 2. Locale from user settings
    user = g.get('user')
    if user and user.get('locale') in app.config['LANGUAGES']:
        return user.get('locale')

    # 3. Locale from request header
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.before_request
def before_request():
    """Executed before all other functions, to check if a user is logged in"""
    g.user = get_user()


@app.route('/')
def index():
    """Route for the index page"""
    return render_template('6-index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
