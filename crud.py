from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menu_section_id = db.Column(db.Integer)
    menu_section = db.Column(db.String(80))
    menu_items = db.Column(db.String(80))

    def __init__(self, menu_section, menu_items, menu_section_id=0):
        self.menu_section = menu_section
        self.menu_items = menu_items
        self.menu_section_id = menu_section_id


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'menu_section', 'menu_items', 'menu_section_id')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

'''
A POST request to make a new item value and add it to the database
@:returns A JSON object, the menu item added to the database
'''


@app.route("/menu", methods=["POST"])
def add_menu_item():
    menu_section = request.json['menu_section']
    menu_item_individual = request.json['menu_item']
    menu_section_id = request.json['menu_section_id']
    new_menu_item = Menu(menu_section, menu_item_individual, menu_section_id)
    db.session.add(new_menu_item)
    db.session.commit()
    return user_schema.jsonify(new_menu_item)


'''
A GET request to get all the menu items in the database
@:returns A JSON object list of all the menu items in the database
'''


@app.route("/menu", methods=["GET"])
def get_menu():
    all_menu_items = Menu.query.order_by(Menu.menu_section).all()
    result = users_schema.dump(all_menu_items)
    return jsonify(result.data)


'''
A GET request to get a specific menu item by id
@:returns A JSON object, the menu item requested
'''


@app.route("/menu/<id>", methods=["GET"])
def menu_item(id):
    menu_item_individual = Menu.query.get(id)
    return user_schema.jsonify(menu_item_individual)


'''
A GET request to get all menu items filtered by a specific section
@:returns A JSON object list of all the filtered menu items
'''


@app.route("/menu/section", methods=["GET"])
def menu_item_section():
    section = request.json['section']
    menu_item = Menu.query.filter_by(menu_section=section)
    return users_schema.jsonify(menu_item)


'''
A PUT request to update a menu item using the id as an identifier
@:returns The updated menu item
'''


@app.route("/menu/<id>", methods=["PUT"])
def menu_item_update(id):
    menu_item_individual = Menu.query.get(id)
    name = request.json['name']

    menu_item_individual.name = name

    db.session.commit()
    return user_schema.jsonify(menu_item_individual)


'''
A DELETE request to delete a menu item by using the id as the identifier
@:returns A JSON object, the item that was deleted
'''


@app.route("/menu/<id>", methods=["DELETE"])
def menu_delete(id):
    menu_item_individual = Menu.query.get(id)
    db.session.delete(menu_item_individual)
    db.session.commit()

    print(user_schema.jsonify(menu_item_individual))
    return user_schema.jsonify(menu_item_individual)


if __name__ == '__main__':
    app.run()