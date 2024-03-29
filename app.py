from flask import Flask, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Playlist, Song, PlaylistSong
from forms import NewSongForPlaylistForm, SongForm, PlaylistForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///playlist-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route("/")
def root():
    """Homepage: redirect to /playlists."""

    return redirect("/playlists")


##############################################################################
# Playlist routes


@app.route("/playlists")
def show_all_playlists():
    """Return a list of playlists."""

    playlists = Playlist.query.all()
    
    return render_template("playlists.html", playlists=playlists)


@app.route("/playlists/<int:playlist_id>")
def show_playlist(playlist_id):
    """Show detail on specific playlist."""
    playlist = Playlist.query.get_or_404(playlist_id)
    playlist_songs = PlaylistSong.query.filter_by(playlist_id=playlist_id)
    
    
    return render_template('playlist.html', playlist=playlist, playlist_songs=playlist_songs)


@app.route("/playlists/add", methods=["GET", "POST"])
def add_playlist():
    """Handle add-playlist form:

    """
    form = PlaylistForm()
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        playlist = Playlist(name=name, description=description)
        db.session.add(playlist)
        db.session.commit()
        return redirect('/playlists')
    else:
        return render_template('new_playlist.html', form=form)
##############################################################################
# Song routes


@app.route("/songs")
def show_all_songs():
    """Show list of songs."""

    songs = Song.query.all()
    return render_template("songs.html", songs=songs)


@app.route("/songs/<int:song_id>")
def show_song(song_id):
    """return a specific song"""
    song = Song.get_or_404(song_id)
    songs = Song.query.all()
    return render_template('song.html', song=song, songs=songs)
    # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK


@app.route("/songs/add", methods=["GET", "POST"])
def add_song():
    """Handle add-song form:

    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-songs
    """
    form = SongForm()
    if form.validate_on_submit():
        title = form.title.data
        artist = form.artist.data
        song = Song(title=title, artist=artist)
        db.session.add(song)
        db.session.commit()
        return redirect('/songs')
    else:
        return render_template('new_song.html', form=form)
    


@app.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
def add_song_to_playlist(playlist_id):
    """Add a song to playlist and redirect to list."""

    # BONUS - ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK

    # THE SOLUTION TO THIS IS IN A HINT IN THE ASSESSMENT INSTRUCTIONS

    playlist = Playlist.query.get_or_404(playlist_id)
    form = NewSongForPlaylistForm(obj=playlist)

    # Restrict form to songs not already on this playlist

    curr_on_playlist = db.session.query(Song.id, Song.title)
    form.song.choices = curr_on_playlist

    if form.validate_on_submit():
        playlist_id = playlist.id
        song = form.song.data
        playlistsong = PlaylistSong(playlist_id=playlist_id, song_id=song)
        db.session.add(playlistsong)
        db.session.commit()
          # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK
        return redirect(f"/playlists/{playlist_id}")

    return render_template("add_song_to_playlist.html",
                             playlist=playlist,
                             form=form)
