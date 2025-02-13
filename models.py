from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    mfa_enabled = db.Column(db.Boolean, default=False, nullable=False)
    mfa_secret = db.Column(db.String(120))
    backup_codes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def generate_backup_codes(self, count=8):
        import secrets
        codes = [secrets.token_hex(8) for _ in range(count)]
        self.backup_codes = ",".join(codes)
        return codes


class PreKey(db.Model):
    __tablename__ = 'prekeys'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    key_id = db.Column(db.Integer, nullable=False)
    public_key = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
