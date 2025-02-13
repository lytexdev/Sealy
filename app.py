from flask import Flask, render_template
from flask_cors import CORS
from config import Config

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config.from_object(Config)
db.init_app(app)

CORS(app, resources={r"/api/*": {"origins": Config.CORS_ORIGINS}})

@app.after_request
def add_header(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
    return response

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def index(path):
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
