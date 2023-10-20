import requests
from flask import Flask, request, redirect, jsonify, render_template
from oauth import Oauth
from data.db import cursor

app = Flask(__name__)

API_KEY = '51fa23e3-950d-4a71-9d92-907c2cd76845'

header = {'accept': 'application/json', 'Authorization': f'Bearer {API_KEY}'}
url = 'https://open.faceit.com/data/v4'

def faceit_get_player_elo(steamid: int):
    response = requests.get(url + f'/players?game=csgo&game_player_id={steamid}', headers=header)

    try:
        return response.json()['games']['cs2']['skill_level']
    except KeyError:
        return False

@app.route("/", methods=["get"])
def index():
    return render_template("index.html")

@app.route("/login", methods=["get"])
def login_redirect():
    return redirect(f"{Oauth.discord_login_url}")

@app.route("/login/oauth", methods=["get"])
def login():
    code = request.args.get("code")
    at = Oauth.get_access_token(code)

    user_info = Oauth.get_user_json(at)
    connections = Oauth.get_user_connections(at)

    user_id = user_info['id']
    steam_data = [connection["id"] for connection in connections if connection["type"] == "steam"]

    cursor.execute("SELECT user_id FROM connections WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()

    if user:
        cursor.execute("UPDATE connections SET steam = %s WHERE user_id = %s", (steam_data[0] if steam_data else None, user_id,))
    else:
        cursor.execute("INSERT INTO connections (user_id, steam) VALUES (%s, %s)", (user_id, steam_data[0] if steam_data else None,))

    return redirect("https://yacheru.ru")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000", debug=True)