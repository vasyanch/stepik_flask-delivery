import csv
import os

from app import db
from models import Category, Dish


def insert_test_data():
    all_objects = []
    with open('delivery_categories.csv', encoding='utf8') as categories_file:
        categories = csv.reader(categories_file, delimiter=',')
        categories_objs = []
        for i, row in enumerate(categories):
            if i == 0:
                continue
            categories_objs.append(Category(id=int(row[0]), title=row[1]))
    all_objects.extend(categories_objs)

    with open('delivery_items.csv', encoding='utf8') as dishes_file:
        dishes = csv.reader(dishes_file, delimiter=',')
        dishes_objs = []
        for i, row in enumerate(dishes):
            if i == 0:
                continue
            dishes_objs.append(
                Dish(
                    id=int(row[0]), title=row[1], price=int(row[2]), description=row[3],
                    picture=os.path.join('/static/images', row[4]),
                    categories=list(filter(lambda x: x.id == int(row[5]), categories_objs))
                )
            )
    all_objects.extend(dishes_objs)

    db.session.add_all(all_objects)
    db.session.commit()


revision = 'insetestdata'
down_revision = '2f182d32410d'
branch_labels = None
depends_on = None


def upgrade():
    insert_test_data()
