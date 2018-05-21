from flask import Flask, render_template, request, abort, jsonify
# from google.appengine.ext import ndb
# from google.cloud import datastore
import stalldb

app = Flask(__name__)
postkey = "asdfasdfasdfasdf"


# Data Model
# todo: since this is not a real db, these 'connections' are not stateless yet

room_config = stalldb.RoomConfig()
stall_status = stalldb.StallStatus()
stall_review = stalldb.StallReview()


# Pages and Routes

@app.route("/")
def index():
  # return repr("asf")
  # return repr(stall_review.get_stalls_review_avg())
  # return repr(stall_status.get_stalls_latest())
  return render_template('index.html', room_config_layout=room_config.get_layout())


@app.route('/get/stallslatest', methods=['GET'])
def get_stalls_latest():
  return jsonify(stall_status.get_stalls_latest())


@app.route('/get/stallsreview', methods=['GET'])
def get_stalls_review():
  return jsonify(stall_review.get_stalls_review_avg())


@app.route('/update/stallstatus', methods=['POST'])
def update_stall_status():
  # global stall_status
  # first check for auth
  if(request.form.get('postkey') != postkey):
    abort(403)

  # look for required args
  if(not (request.form.get('location') and request.form.get('busy'))):
    abort(400)

  # insert into db
  ret = stall_status.update_stall(request.form.get('location'),
                                  request.form.get('busy'))
  print(repr(request.form))
  if(ret):
    return "ok"
  else:
    abort(400)


@app.route('/update/stallrating', methods=['POST'])
def update_stall_rating():
  # global stall_review
  # first check for auth
  if(request.form.get('postkey') != postkey):
    abort(403)

  # look for required args
  if(not (request.form.get('location') and request.form.get('review'))):
    abort(400)

  # insert into db
  ret = stall_review.update_stall_review(request.form.get('location'),
                                         request.form.get('review'))
  if(ret):
    return "ok"
  else:
    abort(400)

