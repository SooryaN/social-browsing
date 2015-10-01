#!flask/bin/python
import os
from flask import Flask, jsonify, abort, request, make_response, url_for, g
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, static_url_path="")
auth = HTTPBasicAuth()
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

from models import *


@auth.verify_password
def verify_password(username_or_token, password):
    user = User.query.filter_by(username=username_or_token).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


@app.route('/api/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)    # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)    # existing user
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201,
            {'Location': url_for('get_user', id=user.id, _external=True)})


@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})

@app.route('/api/users/remove/<string:uname>')
def del_user(uname):
    print "uname",uname
    user = User.query.filter_by(username == uname)
    if not user:
        abort(400)
    else:
        name = user[0].username
        user.delete()
        db.session.commit()
    return jsonify({'username': name})

@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)
    # return 403 instead of 401 to prevent browsers from displaying the
    # default auth dialog


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/api/<string:uname>/history', methods=['GET'])
@auth.login_required
def get_user_history():
    return jsonify({'history': g.user.history})


# @app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
# @auth.login_required
# def get_task(task_id):
#     task = filter(lambda t: t['id'] == task_id, tasks)
#     if len(task) == 0:
#         abort(404)
#     return jsonify({'task': make_public_task(task[0])})

@app.route('/api/visit', methods=['POST'])
@auth.login_required
def add_to_visited():
    if not request.json:
        abort(400)
    else:
        userid = g.user.username
        host =  request.json['host']
        url =  request.json['url']
        time =  datetime.now()
        visit = Visited_logs(userid, url, host, time)
        db.session.add(visit)
        db.session.commit()

    return jsonify({'comment': comment}), 201

@app.route('/api/pageData/<string:url>', methods=['GET'])
def return_pagedata(url):
    visits = Visited_logs.query.filter_by(url = url)
    ret = []
    for u in session.query(User).all():
        u = u.__dict__
        u.pop('_sa_instance_state',0)
        ret.append(u)
    return jsonify({'url': url,'visits': ret}), 201



@app.route('/api/comment', methods=['POST'])
@auth.login_required
def create_task():
    if not request.json:
        abort(400)
    else:
        userid = g.user.username
        title =  request.json['title']
        comment =  request.json['comment']
        url =  request.json['url']
        time =  datetime.now()
        comment = Comment(userid, comment, time, url)
        db.session.add(comment)
        db.session.commit()

    return jsonify({'comment': comment}), 201


if __name__ == '__main__':
    if not os.path.exists('db.sqlite'):
        db.create_all()
    app.run(debug=True)
