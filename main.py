import flask
from flask_sqlalchemy import SQLAlchemy


app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:5433@localhost/lab_7'
db = SQLAlchemy(app)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(512), nullable=False)

    def __init__(self, author, books):
        self.author = author
        self.books = [
            Book(text=book) for book in books.split(',')
        ]


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(32), nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    author = db.relationship('Author', backref=db.backref('books', lazy=True))


@app.route('/', methods=['GET'])
def hello():
    return flask.render_template('index.html', messages=Author.query.all())


@app.route('/add_book', methods=['POST'])
def add_book():
    text = flask.request.form['author']
    tag = flask.request.form['book']
    # messages.append(Message(text, tag))
    db.session.add(Author(text, tag))
    db.session.commit()

    return flask.redirect(flask.url_for('hello'))


with app.app_context():
    db.create_all()
app.run()