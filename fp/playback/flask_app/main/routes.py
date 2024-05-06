from flask import Blueprint, render_template, url_for, redirect, request
from ..models import User, Review
from flask_login import current_user
from ..utils import current_time
import base64,io

from .. import spotify_client
from ..forms import SearchForm, AlbumReviewForm

def get_b64_img(username):
    user = User.objects(username=username).first()
    bytes_im = io.BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image


main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("main.query_results", query=form.search_query.data))
    
    return render_template("index.html", form=form)

@main.route("/search-results/<query>", methods = ["GET"])
def query_results(query):
    try:
        results = spotify_client.seach_for_artist_info(query)
    except ValueError as e:
        return render_template("query.html", error_msg=str(e))

    return render_template("query.html", results=results)

@main.route("/artists/<artist_id>", methods=["GET"])
def artist_detail(artist_id):
    try:
        artist_name = spotify_client.get_artist_info_by_artist_id(artist_id)["name"]
        artist_albums = spotify_client.get_albums_info_by_artist_id(artist_id)
    except ValueError as e:
        return render_template("artist_detail.html", error_msg=str(e))
    return render_template("artist_detail.html", artist_name=artist_name, artist_albums=artist_albums)

@main.route("/albums/<album_id>", methods=["GET", "POST"])
def album_detail(album_id):
    try:
        tracks = spotify_client.get_track_info_by_album_id(album_id)
        album_name = spotify_client.get_album_info_by_album_id(album_id)["name"]
        album_art = spotify_client.get_album_info_by_album_id(album_id)["images"][0]["url"]
        access_token = spotify_client.get_access_token()
    except ValueError as e:
        return render_template("album_detail.html", error_msg=str(e))
    
    form = AlbumReviewForm()
    if form.validate_on_submit():
        review = Review(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            date=current_time(),
            album_id=album_id,
            album_title=album_name,
        )

        review.save()

        return redirect(request.path)

    reviews = Review.objects(album_id=album_id)

    return render_template("album_detail.html", tracks=tracks, 
                           album_name=album_name, reviews=reviews, 
                           form=form, album_art=album_art, 
                           access_token=access_token)

@main.route("/user/<username>")
def user_detail(username):
    #uncomment to get review image
    #user = find first match in db
    user = User.objects(username=username).first()
    #img = get_b64_img(user.username) use their username for helper function
    img = get_b64_img(user.username)
    error = None
    return render_template('user_detail.html', image = img, error = error, username=username)
