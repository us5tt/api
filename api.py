from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_sqlalchemy import SQLAlchemy
# from datatime import datatime

app = Flask(__name__)
api = Api(app)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///allpars.db'
db = SQLAlchemy(app)


ITEMS = {
    'list1': {'task': 'build an API'},
    'list2': {'task': '?????'},
    'list3': {'task': 'test3!'},
    'list4': {'task': 'test4'},
    'list5': {'task': 'test5!'},
}


class Parseritem(db.Model):
    __tablename__ = 'parseitems'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    usd_price = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text(500), nullable=False)
#    date = db.Column(db.DateTime, default=data)



@app.route('/')
def home():
    return 'А тут нічого!, Модель знаходиться: api/v1/items'


def abort_if_list_doesnt_exist(list_id):
    if list_id not in ITEMS:
        abort(404, message="List {} doesn't exist".format(list_id))


parser = reqparse.RequestParser()
parser.add_argument('task')


# клас Item
# методи 'get_id', 'DELETE', 'PUT'
class Item(Resource):
    def get(self, list_id):
        abort_if_list_doesnt_exist(list_id)
        return ITEMS[list_id]

    def delete(self, list_id):
        abort_if_list_doesnt_exist(list_id)
        del ITEMS[list_id]
        return '', 204

    def put(self, list_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        ITEMS[list_id] = task
        return task, 201


# клас ItemList
# показує весь список 'GET', добавляє нові дані до табліці 'POST'
class ItemList(Resource):
    def get(self):
        return ITEMS

    def post(self):
        args = parser.parse_args()
        list_id = int(max(ITEMS.keys()).lstrip('list')) + 1
        list_id = 'list%i' % list_id
        ITEMS[list_id] = {'task': args['task']}
        return ITEMS[list_id], 201


# Налаштовую маршрутизацію ресурсів api
#
api.add_resource(ItemList, '/api/v1/item')
api.add_resource(Item, '/api/v1/item/<list_id>')


if __name__ == '__main__':
    app.run(debug=True)