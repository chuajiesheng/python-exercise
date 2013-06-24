#!/usr/bin/python -tt
# todo.py

# vim: smartindent expandtab tabstop=4 shiftwidth=4 softtabstop=4
import sys
import csv
import json

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

def add_to_db(t):
    db.session.add(Item(text=t))
    db.session.commit()
    print 'adding', t

def add_object_to_db(i):
    db.session.add(i)
    db.session.commit()
    print 'added', i.text

def list_all():
    items = Item.query.all()
    for item in items:
        status = '[x]' if item.done else '[ ]'
        print item.id, status, item.text
    if len(items) == 0:
        print 'no item in list'

def mark_as_done(id):
    item = Item.query.get(id)
    item.done = True
    db.session.commit()

def delete(id):
    item = Item.query.get(id)
    db.session.delete(item)
    db.session.commit()

def delete_all():
    for item in Item.query.all():
        db.session.delete(item)
    db.session.commit()

def delete_done():
    for item in Item.query.all():
        if (item.done == True):
            db.session.delete(item)
    db.session.commit()

def out_to_csv():
    writer = csv.writer(sys.stdout)
    writer.writerow(['id', 'done', 'text'])
    for item in Item.query.all():
        writer.writerow([item.id, 'y' if item.done else '', item.text])

def load_csv(file):
    with open(file, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:         
            add_object_to_db(Item(text=row['text'], done=row['done']=='y'))

def out_to_json():
    data = []
    for item in Item.query.all():
        data.append({
                'id': item.id,
                'done': item.done,
                'text': item.text,
                })
    print json.dumps(data, indent=2)

def load_json():
    list = json.load(sys.stdin)
    for i in list:
        add_object_to_db(Item(text=i['text'], done=i['done']))

def main():
    cmd = sys.argv[1]
    if cmd == 'add':
        add_to_db(sys.argv[2])
    elif cmd == 'csv':
        out_to_csv()
    elif cmd == 'loadcsv':
        load_csv(sys.argv[2])
    elif cmd == 'delete':
        id = int(sys.argv[2])
        delete(id)
        list_all()
    elif cmd == 'delete-all':
        delete_all()
    elif cmd == 'cleanup':
        delete_done()
        list_all()
    elif cmd == 'done':
        id = int(sys.argv[2])
        mark_as_done(id)
        list_all()
    elif cmd == 'json':
        out_to_json()
    elif cmd == 'loadjson':
        load_json()
    elif cmd == 'list':
        list_all()
    else:
        print 'unknown command'

if __name__ == '__main__':
    app.app_context().push()
    db.create_all()
    main()

