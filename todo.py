#!/usr/bin/python -tt
# todo.py

# vim: smartindent expandtab tabstop=4 shiftwidth=4 softtabstop=4
import sys
import csv

# flask import
import flask
from flask.ext.sqlalchemy import SQLAlchemy
app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)
# end flask import

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    done = db.Column(db.Boolean)

def add_to_db():
    if len(sys.argv) > 2:
        t = sys.argv[2]
        db.session.add(Item(text=t))
        db.session.commit()
        print 'adding', t

def out_to_csv():
    writer = csv.writer(sys.stdout)
    writer.writerow(['id', 'done', 'text'])
    for item in Item.query.all():
        writer.writerow([item.id, 'y' if item.done else '', item.text])

def main():
    cmd = sys.argv[1]
    if cmd == 'add':
        add_to_db()
    elif cmd == 'csv':
        out_to_csv()
    elif cmd == 'delete':
        id = int(sys.argv[2])
        item = Item.query.get(id)
        db.session.delete(item)
        db.session.commit()
    elif cmd == 'delete-all':
        for item in Item.query.all():
            db.session.delete(item)
        db.session.commit()
    elif cmd == 'done':
        id = int(sys.argv[2])
        item = Item.query.get(id)
        item.done = True
        db.session.commit()
    elif cmd == 'list':
        for item in Item.query.all():
            status = '[x]' if item.done else '[ ]'
            print item.id, status, item.text
    else:
        print 'unknown command'

    

if __name__ == '__main__':
    app.app_context().push()
    db.create_all()
    main()

