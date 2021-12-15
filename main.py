from flask import Flask, render_template, redirect, request
from musixmatch import Musixmatch
import requests, logging, json, encode as e

redirect_uri = e.callback
app = Flask(__name__)

# Move to environment variables
musixmatch = Musixmatch(e.musixmatch)
spotify_client_id = e.spotify_client_id
spotify_client_secret = e.spotify_client_secret

logging.basicConfig(level=logging.DEBUG)

@app.route("/")
def index():
   return render_template("index.html")

@app.route("/about")
def about():
   return render_template("about.html")

@app.route("/login")
def request_user_auth():
  """Request authorization from user."""
  app.logger.info('Requesting Auth')
  login_url = f"https://accounts.spotify.com/authorize?client_id={spotify_client_id}&response_type=code&scope=user-top-read&redirect_uri={redirect_uri}"
  return redirect(login_url)


@app.route("/callback")
def callback():
  """Recieve access token from Spotify."""
  code = str(request.query_string).split("=")[-1][:-1]
  
  request_body = {"grant_type": "authorization_code", "code": code, "redirect_uri": redirect_uri, "client_id": spotify_client_id, "client_secret": spotify_client_secret}
  token = requests.post(url="https://accounts.spotify.com/api/token", data=request_body, headers={"Content-Type": "application/x-www-form-urlencoded"}).json()['access_token']
  
  user_top = requests.get(url="https://api.spotify.com/v1/me/top/tracks/?limit=30", headers={"Authorization": f"Bearer {token}", "Content-Type":"application/json"}).json()
  app.logger.info("Data obtained")
  
  top_songs = []
  for song in user_top["items"]:
    song_name = song["name"]
    artist = song["artists"][0]["name"]
    if len(song_name) == 0 or len(artist) == 0:
      continue
    else:
      top_songs.append([song_name, artist])
  
  app.logger.info("Found Top Songs")
  if len(top_songs) == 0:
    return render_template("failure.html")

  snippets = []
  for i in top_songs:
    curr_track = i[0] + ", " + i[1]
    song = i[0]
    artist = i[1]
    info = musixmatch.matcher_track_get(song, artist)
    if info['message']['header']['status_code'] != 200 or info['message']['body']['track']['has_lyrics'] != 1:
      continue
    else:
      id = info['message']['body']['track']['track_id']
      snippet = musixmatch.track_snippet_get(id)['message']['body']['snippet']['snippet_body']
      app.logger.info(snippet)
      if snippet == "" or snippet == "null":
        continue
      else:
        snippets.append([snippet, curr_track])
  app.logger.info('Found', len(snippets), 'Snippets')
  if len(snippets) == 0:
    return render_template("failure.html")
  else:
    return render_template("quiz.html",snippets=json.dumps(snippets))

@app.route('/offline')
def offline():
  snippets = [["Don't let, don't let the lifestyle drag you down", "Believe What I Say - Kanye West"], ["I'm off, on the adventure", "Mr. Rager - Kid Cudi"], ["No more, promos, No more, photos, No more, logos, No more, chokeholds", "Heaven and Hell - Kanye West"], ["And I know you wouldn't leave", "Wouldn't Leave - Kanye West"]]
  return render_template("quiz.html",snippets=json.dumps(snippets))


if __name__ == "__main__":
  host = '0.0.0.0'
  port = '6378'
  debug = "True"
  app.run(host = host, port = port, debug = debug)