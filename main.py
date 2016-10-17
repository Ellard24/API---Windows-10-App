#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from flask import Flask, jsonify
from flask import request 
import json
from google.appengine.api import urlfetch
from google.appengine.ext import ndb

import models, helperFunctions



app = Flask(__name__)




@app.route("/", methods=['GET'])
def viewAll():
	
	allUsers = helperFunctions.allUsers()
	allInboxes = helperFunctions.allInboxes()
	
	return jsonify({'Users': allUsers, 'Inboxes': allInboxes})


@app.route("/location/<int:userID>/", methods=['PUT'])
def updatedLocation(userID):
	if request.method == 'PUT':
		return json.dumps(helperFunctions.updateLocation(userID, request.form))
	
@app.route("/users/<int:userID>/", methods=['GET', 'PUT', 'DELETE'])
def getUser(userID):
	if request.method == 'GET':
		retUser = helperFunctions.getUser(userID)
		return json.dumps(retUser)
		#might need to include an error catcher here
		
	if request.method == 'PUT':
		updatedUser= helperFunctions.updateUser(userID,request.form)
		return json.dumps(updatedUser)
		
	if request.method == 'DELETE':
		return json.dumps(helperFunctions.deleteUser(userID))

@app.route("/users/", methods=['GET','POST'])
def userHandler():
		if request.method == 'GET':
			return json.dumps(helperFunctions.allUsers())
		else:
			return json.dumps(helperFunctions.createUser(request.form))

			

@app.route("/inbox/", methods=['GET', 'POST'])			
def inboxHandler():
	if request.method == 'GET':
		return json.dumps(helperFunctions.allInboxes())
	else:
		return json.dumps(helperFunctions.createInbox(request.form))
		

@app.route("/inbox/<int:userID>/", methods=['GET'])
def inboxViewer(userID):
	if request.method == 'GET':
		return json.dumps(helperFunctions.getInboxes(userID))


@app.route("/letter/", methods=['POST'])
def letterHandler():
	if request.method == 'POST':
		return json.dumps(helperFunctions.createLetter(request.form))

@app.route("/letter/<int:inboxID>/", methods = ['GET'])
def letterViewer(inboxID):
	if request.method == 'GET':
		return json.dumps(helperFunctions.getLetters(inboxID))

@app.route("/deleteLetter/<int:letterID>/", methods=['DELETE'])
def deleteLetterHandler(letterID):
	if request.method == 'DELETE':
		return json.dumps(helperFunctions.deleteLetter(letterID))

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return "Sorry, Nothing at this URL.", 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return "Sorry, unexpected error: {}".format(e), 500
	

