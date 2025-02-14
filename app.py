from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, join_room
from config import Config
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from extensions import db
from models import User, Message

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
    
    access_token = create_access_token(identity=str(user.id))
    return jsonify({'access_token': access_token, 'user_id': user.id}), 200

@app.route('/api/users', methods=['GET'])
@jwt_required()
def get_users():
    current_user_id = get_jwt_identity()
    users = User.query.filter(User.id != int(current_user_id)).all()
    user_list = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
    return jsonify(user_list), 200

@app.route('/api/messages/<int:other_user_id>', methods=['GET'])
@jwt_required()
def get_messages(other_user_id):
    current_user_id = int(get_jwt_identity())
    
    messages = Message.query.filter(
        ((Message.sender_id == current_user_id) & (Message.recipient_id == other_user_id)) |
        ((Message.sender_id == other_user_id) & (Message.recipient_id == current_user_id))
    ).order_by(Message.created_at).all()
    
    messages_list = [{
        "id": m.id,
        "sender_id": m.sender_id,
        "recipient_id": m.recipient_id,
        "ciphertext": m.ciphertext,
        "iv": m.iv,
        "created_at": m.created_at.isoformat()
    } for m in messages]
    return jsonify(messages_list), 200

@socketio.on('join')
def on_join(data):
    user_id = data.get('user_id')
    if user_id:
        join_room(str(user_id))

@socketio.on('send_message')
def handle_send_message(data):
    sender_id = data.get("sender_id")
    recipient_id = data.get("recipient_id")
    ciphertext = data.get("message")
    iv = data.get("iv")
    
    if sender_id and recipient_id and ciphertext and iv:
        msg = Message(sender_id=int(sender_id), recipient_id=int(recipient_id), ciphertext=ciphertext, iv=iv)
        db.session.add(msg)
        db.session.commit()
    socketio.emit('receive_message', data, room=str(recipient_id))


def create_db():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    create_db()
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
