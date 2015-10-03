#!flask/bin/python
import os
from flask import Flask, jsonify, abort, request, make_response, url_for, g
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from flask.ext.cors import CORS, cross_origin

app = Flask(__name__, static_url_path="")
auth = HTTPBasicAuth()
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
from models import *
annotations = []


@auth.verify_password
def verify_password(username, token):
    user = User.query.filter_by(username=username).first()
    if not user or token != user.token:
        return False
    g.user = user
    return True


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


@app.route('/api/dummytest')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.name})


@app.route('/user', methods=['POST'])
def new_user():
    name = request.json['name']
    fbuserid = request.json['fbuserid']
    friends = request.json['friends']
    if username is None or fbuserid is None:
        abort(400)    # missing arguments
    if User.query.filter_by(fbuserid=fbuserid).first() is not None:
        abort(400)    # existing user
    user = User(fbuserid, name, friends)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'name': user.name, 'fbuserid': user.fbuserid}), 201,
            {'Location': url_for('get_user', id=user.id, _external=True)})


@app.route('/users/<string:fbid>')
def get_user(fbid):
    user = User.query.filter_by(fbuserid=fbid)
    if not user:
        abort(400)
    user = user.__dict__
    user.pop('_sa_instance_state', 0)
    return jsonify({'user': user})


@app.route('/users/remove/<string:fbid>')
def del_user(fbid):
    user = User.query.filter_by(fbuserid=fbid)
    if not user:
        abort(400)
    else:
        name = user[0].name
        user.delete()
        db.session.commit()
    return jsonify({'name': name})

# @app.route("/annotator")
# @cross_origin()
# def helloWorld():
#   return "Hello, cross-origin-world!"

# @app.route("/annotator/search")
# @cross_origin()
# def helloWorld1():

#   a =jsonify({"total":len(annotations),"rows":annotations})
#   print a
#   return a

# @app.route("/annotator/annotations", methods = ['POST'])
# @cross_origin()
# def helloWorld2():
#     annotations.append(dict(request.json))
#     print annotations
#     return jsonify({"success":"Added"})


# returns user history
@app.route('/visited', methods=['GET'])
# @auth.login_required
def get_user_history(uid):
    try:
        userid = g.user.fbuserid
    except:
        abort(403)
    allVisits = Visited_logs.query.all()
    pagelist = set()
    pages = {}
    for i in allVisits:
        if userid == i.fbuserid:
            pagelist.add(i.url)
    for url in pagelist:
        pageHistory = []
        for v in Visited_logs.query.filter_by(url=url).filter_by(fbuserid=userid):
            v = v.__dict__
            v.pop('_sa_instance_state', 0)
            pageHistory.append(v)
        pages[i.url] = pageHistory

    return jsonify({'fbuserid': userid, 'pages': pages})

# Logs in the logged in user's visit to a page


@app.route('/visited', methods=['POST'])
@auth.login_required
def add_to_visited():
    visit = Visited_logs.query.filter_by(fbuserid=g.user.fbuserid).first()
    visit.endtime = datetime.fromtimestamp(int(request.json['endViewTime']))
    visit.time_spent = (visit.endtime - visit.starttime).total_seconds()
    db.session.commit()
    return jsonify({'Status': 'Changed'}), 200

# Add user visit to db


@app.route('/visited/history', methods=['POST'])
@auth.login_required
def add_to_visited():
    if not request.json:
        print request.json
        abort(400)
    else:
        userid = g.user.fbuserid
        url = request.json['url']
        try:
            host = request.json['host']
        except:
            host = 'http://'+url.split('/')[2]

        viewTime = datetime.fromtimestamp(int(request.json['viewTime']))
        endViewTime = datetime.fromtimestamp(int(request.json['viewTime']))
        time_spent = 0
        # time_spent = time_spent.total_seconds()

        visit = Visited_logs(
            userid, url, host, viewTime, endViewTime, time_spent)

        db.session.add(visit)
        db.session.commit()

        visits = Visited_logs.query.filter_by(url=url)
        users = set()

        for i in visits:
            users.add(i.fbuserid)

        visitsList = []
        commentsList = []

        for u in User.query.all():
            if u.fbuserid in users:
                u = u.__dict__
                u.pop('_sa_instance_state', 0)
                visitsList.append(u)
        comments = Comments.query.filter_by(url=url)

        for c in comments:
            c = c.__dict__
            c.pop('_sa_instance_state', 0)
            commentsList.append(c)

    return jsonify({'url': url, 'visits': visitsList, 'comments': commentsList}), 201


@app.route('/visited/<int:visitid>', methods=['DELETE'])
@auth.login_required
def delete_page_view(visitid):
    view = Visited_logs.query.filter_by(id=visitid)
    if not view:
        abort(400)
    else:
        view.delete()
        db.session.commit()
    return jsonify({'status': 'Delete Successful'})


# # returns the given url's pageData
# @app.route('/api/pageData', methods=['POST'])
# def return_pagedata():
#     if not request.json:
#         abort(400)
#     url = request.json['url']
#     visits = Visited_logs.query.filter_by(url=url)
#     users = set()
#     for i in visits:
#         users.add(i.userid)
#     visitsList = []
#     commentsList = []
#     for u in User.query.all():
#         if u.username in users:
#             u = u.__dict__
#             u.pop('_sa_instance_state', 0)
#             visitsList.append(u)
#     comments = Comments.query.filter_by(url=url)
#     for c in comments:
#         c = c.__dict__
#         c.pop('_sa_instance_state', 0)
#         commentsList.append(c)
# return jsonify({'url': url, 'visits': visitsList, 'comments':
# commentsList}), 201

# Logs a comment


@app.route('/comments', methods=['POST'])
@auth.login_required
def create_task():
    if not request.json:
        abort(400)
    else:
        userid = g.user.fbuserid
        comment = request.json['comment']
        url = request.json['url']
        time = datetime.now()
        commentObj = Comments(userid, comment, time, url)
        db.session.add(commentObj)
        db.session.commit()
        commentObj = Comments.query.all()[-1]
        commentObj = commentObj.__dict__
        commentObj.pop('_sa_instance_state', 0)

    return jsonify({'comment': commentObj}), 201


@app.route('/comments/<int:commentid>', methods=['DELETE'])
@auth.login_required
def delete_comment(commentid):
    comment = Comments.query.filter_by(id=commentid)
    if not comment:
        abort(400)
    else:
        comment.delete()
        db.session.commit()
    return jsonify({'status': 'Delete Successful'})


@app.route('/messages/<int:receiverid>', methods=['POST'])
@auth.login_required
def send_a_message(receiverid):
    if not request.json:
        abort(400)
    senderid = g.user.id
    if request.json['public'] == "True":
        public = True
    else:
        public = False
    if not public and receiverid not in g.user.friends.split(','):
        abort(400)
    url = request.json['url']
    messageList = request.json['ls']
    if request.json['public'] == "True":
        public = True
    else:
        public = False
    time = datetime.now()
    message = Messages(
        url, senderid, receiverid, messageList, public, time)
    db.session.add(message)
    db.session.commit()
    message = Messages.query.all()[-1]
    message = message.__dict__

    return jsonify({'messageid': message['id']}), 201


@app.route('/messages', methods=['GET'])
@auth.login_required
def view_messages():
    try:
        since = request.get['since']
    except:
        since = datetime.now()
    try:
        limit = request.get['limit']
    except:
        limit = 10
    messageList = []
    messages = Messages.query.limit(limit).all()
    for c in messages:
        if c.time < since:
            c = c.__dict__
            c.pop('_sa_instance_state', 0)
            c.pop('html', 0)
            messageList.append(c)
    return jsonify({'messages': messageList}), 201


@app.route('/messages/seen/<int:messageid>', methods=['POST'])
# @auth.login_required
def open_message(messageid):
    message = Messages.query.filter_by(id=messageid).first()
    message.seen = True
    db.session.commit()
    message = message.__dict__
    message.pop('_sa_instance_state', 0)
    return jsonify({'message': message}), 201


if __name__ == '__main__':
    if not os.path.exists('db.sqlite'):
        db.create_all()
    app.run(debug=True)
