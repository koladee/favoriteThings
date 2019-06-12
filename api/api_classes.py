from flask import request
from flask_restful import Resource
from api import db, bcrypt
from api.models import User, UserSchema, Category, CategorySchema, List, ListSchema
import string
import random
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
import datetime
from flask_login import login_user


users_schema = UserSchema(many=True)
user_schema = UserSchema()
categories_schema = CategorySchema(many=True)
category_schema = CategorySchema()
lists_schema = ListSchema(many=True)
list_schema = ListSchema()


def process(ob):
    title = ob['title']
    description = ob['description']
    category = ob['category']
    ranking = ob['ranking']
    user_id = ob['user_id']
    if title is not None:
        if int(ranking) > 0:
            if category is not None:
                proceed = True
                if description is not None:
                    length = len(description)
                    if length >= 10 or length == 0:
                        proceed = True
                    else:
                        proceed = False
                if proceed is True:
                    exist = List.query.filter(
                        List.ranking >= ranking,
                        List.cat == category, List.user_id == user_id).all()
                    for each in exist:
                        if int(ranking) == int(each.ranking):
                            rank = db.session.query(func.max(List.ranking)). \
                                filter(List.cat == category, List.user_id == user_id).all()
                            each.ranking = int(rank[0][0]) + 1
                        else:
                            # print(each.ranking)
                            each.ranking = each.ranking

                    rand = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])
                    fav = List(rid=rand, title=title, description=description, ranking=ranking, user_id=user_id,
                               cat=category)
                    exist.append(fav)
                    db.session.add_all(exist)
                    done = {
                        "status": False,
                        "message": "Request was successfully added to your favorite list."
                    }
                    try:
                        db.session.commit()
                        done['status'] = True
                    except SQLAlchemyError as e:
                        reason = str(e)
                        done['message'] = reason
                    return done, 201
                else:
                    resp = {
                        "status": "error",
                        "message": "If description is not empty, its content must be greater than or equal"
                                   " to 10 characters"
                    }
                    return resp, 400
            else:
                resp = {
                    "status": "error",
                    "message": 'Oops!!! A category must be selected.'
                }
                return resp, 400
        else:
            resp = {
                "status": "error",
                "message": 'Oops!!! The ranking field is required and it must be greater than zero in value.'
            }
            return resp, 400
    else:
        resp = {
            "status": "error",
            "message": 'Oops!!! The title fields is required.'
        }
        return resp, 400


class Users(Resource):
    def get(self):
        if not request.args.get('email'):
            # return the list of users
            users = User.query.all()
            users = users_schema.dump(users).data
            return {'status': 'success', 'data': users}, 200
        else:
            json_data = {}
            json_data['email'] = request.args.get('email')
            json_data['password'] = request.args.get('password')
            users = User.query.filter_by(email=json_data['email']).first()
            if users:
                if users and bcrypt.check_password_hash(users.password, json_data['password']):
                    # login user
                    login_user(users)
                    users = user_schema.dump(users).data
                    return {'status': 'success', 'data': users}, 200
                else:
                    return {'status': 'error', 'message': "Email address or password is incorrect."}, 200
            else:
                return {'status': 'error', 'message': "The user with this email address does not exist."}, 200

    def post(self):
        # insert into db
        json_data = request.get_json(force=True)
        if not json_data:
            return {'status': 'error', 'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = user_schema.load(json_data)
        if errors:
            return errors, 422
        user = User.query.filter_by(email=data['email']).first()
        if user:
            return {'status': 'error', 'message': 'Oops! Email address already exists.'}, 400
        passw = bcrypt.generate_password_hash(json_data['password']).decode('utf-8')
        user = User(username=json_data['username'], email=json_data['email'], password=passw)
        db.session.add(user)
        db.session.commit()
        resp = user_schema.dump(user).data
        return {"status": 'success', 'data': resp}, 201

    def put(self):
        # update users details
        json_data = request.get_json(force=True)
        if not json_data:
            return {"status": 'error', 'message': 'User id is required'}, 400
        # Validate and deserialize input
        data, errors = user_schema.load(json_data)
        if errors:
            return errors, 422
        user = User.query.filter_by(id=data['id']).first()
        if not user:
            return {"status": 'error', 'message': 'User does not exist'}, 400
        user.name = data['name']
        db.session.commit()
        resp = user_schema.dump(user).data
        return {"status": 'success', 'data': resp}, 204


class Cats(Resource):
    def get(self):
        if not request.args.get('user'):
            # return the list of categories
            cats = Category.query.all()
            cats = categories_schema.dump(cats).data
            return {'status': 'success', 'data': cats}, 200
        else:
            user = int(request.args.get('user'))
            cat1 = Category.query.filter_by(id=1).first()
            cat2 = Category.query.filter_by(id=2).first()
            cat3 = Category.query.filter_by(id=3).first()
            cats = Category.query.filter_by(user_id=user).all()
            cats.append(cat1)
            cats.append(cat2)
            cats.append(cat3)
            cats = categories_schema.dump(cats).data
            return {'status': 'success', 'data': cats}, 200


    def post(self):
        # insert into db
        json_data = request.get_json(force=True)
        if not json_data:
            return {'status': 'error', 'message': 'name and user_id fields are required'}, 400
        # Validate and deserialize input
        data, errors = category_schema.load(json_data)
        if errors:
            return errors, 422
        cat = Category.query.filter_by(name=data['name'], user_id=data['user_id']).first()
        if cat:
            return {'status': 'error', 'message': 'This favourite category already exist for you.'}, 400
        cat = Category(name=json_data['name'], user_id=json_data['user_id'])
        db.session.add(cat)
        db.session.commit()
        resp = category_schema.dump(cat).data
        return {"status": 'success', 'data': resp}, 201

    def put(self):
        # update category
        json_data = request.get_json(force=True)
        if not json_data:
            return {"status": 'error', 'message': 'Category id is required'}, 400
        # Validate and deserialize input
        data, errors = category_schema.load(json_data)
        if errors:
            return errors, 422
        cat = Category.query.filter_by(id=data['id']).first()
        if not cat:
            return {"status": 'error', 'message': 'Category does not exist'}, 400
        cat.name = data['name']
        db.session.commit()
        resp = category_schema.dump(cat).data
        return {"status": 'success', 'data': resp}, 204


class FavoriteList(Resource):
    def get(self):
        # return Lists
        if not request.args.get('user') and not request.args.get('id') and not request.args.get('cat'):
            lists = List.query.all()
            lists = lists_schema.dump(lists).data
            return {'status': 'success', 'data': lists}, 200
        else:
            if request.args.get('user'):
                user = int(request.args.get('user'))
                if not request.args.get('cat'):
                    lists = List.query.filter_by(user_id=user).all()
                else:
                    cat = int(request.args.get('cat'))
                    lists = List.query.filter_by(user_id=user, cat=cat).all()
                lists = lists_schema.dump(lists).data
                return {'status': 'success', 'data': lists}, 200
            else:
                if request.args.get('cat') and not request.args.get('id'):
                    cat = int(request.args.get('cat'))
                    lists = List.query.filter_by(cat=cat).all()
                    lists = lists_schema.dump(lists).data
                else:
                    idd = int(request.args.get('id'))
                    lists = List.query.filter_by(id=idd).first()
                    lists = list_schema.dump(lists).data
                return {'status': 'success', 'data': lists}, 200




    def post(self):
        # insert into db
        json_data = request.get_json(force=True)
        # Validate and deserialize input
        data, errors = list_schema.load(json_data)
        if errors:
            return errors, 422
        resp = process(json_data)
        return resp

    def put(self):
        # update favourite list
        json_data = request.get_json(force=True)
        if not json_data:
            return {"status": 'error', 'message': 'List id is required'}, 400
        # Validate and deserialize input
        data, errors = list_schema.load(json_data)
        if errors:
            return errors, 422
        item = List.query.filter_by(id=data['id']).first()
        if not item:
            return {"status": 'error', 'message': 'Category does not exist'}, 400
        # do comparison of old title, desc, cat & ranking to detect any changes
        title = ""
        des = ""
        cate = ""
        rankn = ""
        if item.title != data['title']:
            title = "The title changed from <b>"+item.title+"</b> to <b>"+data['title']+"</b>(+||+)"
        if item.description != data['description']:
            des = "The description changed from <b>"+item.description+"</b> to <b>"+data['description']+"</b>(+||+)"
        if item.cat != data['cat']:
            cat1 = Category.query.filter_by(id=item.cat).first()
            cat2 = Category.query.filter_by(id=data['cat']).first()
            cate = "The category changed from <b>"+cat1.name+"</b> to <b>"+cat2.name+"</b>(+||+)"
        if item.ranking != data['ranking']:
            rankn = "The ranking changed from <b>"+str(item.ranking)+"</b> to <b>"+str(data['ranking'])+"</b>(+||+)"
        # update all other fields apart from ranking
        if title != "" or des != "" or cate != "" or rankn != "":
            item.title = data['title']
            item.description = data['description']
            item.cat = data['cat']
            item.modified_date = db.func.current_timestamp()
            now = datetime.datetime.now()
            time = str(str(now.year)+"-"+str(now.month)+"-"+str(now.day)+"T"+str(now.hour)+":"+str(now.minute)
                       +":"+str(now.second))
            log = str(item.log)
            item.log = str(log+"{:||:}"+title+""+des+""+cate+""+rankn+""+time)
            # implement the ranking algorithm
            ranking = data['ranking']
            category = data['cat']
            exist = List.query.filter(
                List.ranking >= ranking,
                List.cat == category, List.user_id == item.user_id).all()
            for each in exist:
                if int(ranking) == int(each.ranking):
                    rank = db.session.query(func.max(List.ranking)). \
                        filter(List.cat == category, List.user_id == item.user_id).all()
                    each.ranking = int(rank[0][0]) + 1
            item.ranking = data['ranking']
            db.session.commit()
            resp = list_schema.dump(item).data
            return {"status": 'success', 'data': resp}, 204
        else:
            resp = {
                "status": "error",
                "message": 'Oops!!! No changes was made'
            }
            return {"status": 'success', 'data': resp}, 204
