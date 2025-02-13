from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from config import Config
from flask_jwt_extended import JWTManager, create_access_token
from extensions import db
from models import User

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config.from_object(Config)
db.init_app(app)
jwt = JWTManager(app)
socketio = SocketIO(app, cors_allowed_origins=Config.CORS_ORIGINS)
CORS(app, resources={r"/api/*": {"origins": Config.CORS_ORIGINS}})

@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
    return response

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def index(path):
    return render_template("index.html")

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({'msg': 'Missing username, email or password'}), 400
    
    if db.session.query(db.exists().where((User.username == username) | (User.email == email))).scalar():
        return jsonify({'msg': 'Username or email already exists'}), 409
    
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'msg': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'msg': 'Missing username or password'}), 400
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not user.check_password(password):
        return jsonify({'msg': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200

@socketio.on('send_message')
def handle_send_message(data):
    recipient_id = data.get("recipient_id")
    socketio.emit('receive_message', data, room=recipient_id)

def create_db():
    with app.app_context():
        db.create_all()


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
    create_db()
