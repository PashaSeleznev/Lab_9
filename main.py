import sqlalchemy as db
import flask

app = flask.Flask(__name__)

engine = db.create_engine('postgresql://postgres:5433@localhost/lab_9')
connection = engine.connect()

metadata = db.MetaData()

books = db.Table('books', metadata,
                 db.Column('author', db.Text),
                 db.Column('name', db.Text))
metadata.create_all(engine)

query = db.insert(books).values(author='A.Gruber', name='Mark of Death')
Result = connection.execute(query)

#output = connection.execute(books.select()).fetchall()
#print(output)


@app.route('/', methods=['GET'])
def hello():
    return flask.render_template('index.html', messages=books.query.all())



@app.route('/add_book', methods=['POST'])
def add_book():
    add = flask.request.form['add']
    submit = flask.request.form['submit']
    # messages.append(Message(text, tag))
    db.session.add(books(add, submit))
    db.session.commit()

    return flask.redirect(flask.url_for('hello'))

app.run()