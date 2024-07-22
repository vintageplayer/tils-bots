from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Note(db.Model):
    __table_args__ = {"schema":"til"}
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, nullable=True)
    telegram_user_id = db.Column(db.Integer)
    telegram_username = db.Column(db.Text)
    telegram_first_name = db.Column(db.Text)
    telegram_last_name = db.Column(db.Text)
    message_text = db.Column(db.Text)
    telegram_creation_date = db.Column(db.BigInteger)
    _created_at = db.Column(db.BigInteger, server_default=db.FetchedValue())
    _updated_at = db.Column(db.BigInteger, server_default=db.FetchedValue())
