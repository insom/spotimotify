#!/usr/bin/env python
from __future__ import with_statement
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, Blueprint
from appscript import Application

spotimotify = Blueprint('spotimotify', __name__)

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.register_blueprint(spotimotify)
    return app

@spotimotify.route('/', methods=['GET', 'POST'])
def index():
    s = Application('Spotify')
    action = request.form.get('action')
    if action:
        getattr(s, action)()
        return redirect(url_for('.index'))
    track_name = s.current_track.name()
    track_artist = s.current_track.artist()
    track_album = s.current_track.album()
    state = s.player_state()
    del s
    return render_template('index.html',
        state=str(state),
        track_name=track_name,
        track_artist=track_artist,
        track_album=track_album,
    )

app = create_app()

if __name__=="__main__":
    app.run()
