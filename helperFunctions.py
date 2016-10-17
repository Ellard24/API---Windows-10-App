from google.appengine.ext import ndb
import models
import json
import datetime

#User options


#Return specific user 
def getUser(userID):
	
	if ndb.Key(models.User, int(userID)).get() is None:
		return {'error': 'User does not exist'}
	else:
		retUser = ndb.Key(models.User, int(userID)).get().to_dict()
		return retUser
	
#Deletes specific user	
def deleteUser(userID):
	
	if ndb.Key(models.User, int(userID)).get() is None:
		return {'error': 'User does not exist and thus can not be deleted'}
	else:
		try:
			retUser = ndb.Key(models.User, int(userID)).get().key
			retUser.delete()
		except:
			return {'error': 'error during deletion of user'}
		
		return {'Success': 'User deleted'}

#Updates Users Information		
def updateUser(userID, postForm):
	
	#We need to first check to see if the entry already exists. If it does, just update it
	#	otherwise the try clause will fail and we can make a new one
	
		
		
		
	updatedUser = ndb.Key(models.User, int(userID)).get()
	
	
	
	if not postForm['password']:
		return {'error', 'Password required'}
	else:
		updatedUser.password = postForm['password']
		
		updatedUser.put()
		return {'Success': 'Password updated'}
		
		

def updateLocation(userID,postForm):

	updatedUser = ndb.Key(models.User, int(userID)).get()
		
	updatedUser.latitude = postForm['latitude']
	updatedUser.longitude = postForm['longitude']
	updatedUser.put()
	
	return {'Success': 'Location updated'}

def createUser(postForm):
	 
	if 'name' in postForm:
		
		#Check to see if user already exists
		checkUser = models.User.query(models.User.name == postForm['name']).fetch()
		if len(checkUser) > 0:
			return {'error': 'User already exists'}
	
		if not postForm['name']:
			return {'error': 'Name can not be empty string'}
	
		if not postForm['password']:
			return {'error': 'Please give a password'}
		
		
		
		#User doesn't exist thus we can create it 
		newUser = models.User(name=postForm['name'])
		
		newUser.password = postForm['password']
		try:
			newUser.latitude = postForm['lattitude']
			newUser.longitude = postForm['longitude']
		except:
			newUser.latitude = str(0);
			newUser.longitude = str(0);
			
		newUser.date_created = datetime.date.today()
		
		
		
		finalUser = newUser.put()
		
		userID_check = finalUser.get()
		
		userID_check.userID = str(finalUser.id())
		userID_check.put() 
		return {'New User Registered': userID_check.name}
	else:
		return {'error': 'Name can not be empty string.2nd'}

		

'''
Inbox API functions


'''
def createInbox(postForm):
	 
	if 'name' in postForm:
		
		
		#Check to see if user already exists
		checkInbox = models.Inbox.query(models.Inbox.name == postForm['name']).fetch()
		if len(checkInbox) > 0:
			return {'error': 'Inbox already exists'}
	
		if not postForm['name']:
			return {'error': 'Inbox name can not be empty string'}
	
		
		
		
		#User doesn't exist thus we can create it 
		newInbox = models.Inbox(name=postForm['name'])
		
		if not postForm['user']:
			return {'error': 'userID required'}
		

		newInbox.user = ndb.Key(models.User, int(postForm['user']))
		finalInbox = newInbox.put()
		
		
		
		
		
		inbox_check = finalInbox.get()
		inbox_check.inboxID = str(finalInbox.id())
		inbox_check.put() 
		return {'New Inbox Registered': finalInbox.id()}
	else:
		return {'error': 'Name can not be empty string.2nd'}		
		
 

def getInboxes(userID):


	inboxList = [d.to_dict() for d in models.Inbox.query(models.Inbox.user == ndb.Key(models.User, int(userID))).fetch()]
	return inboxList


	
#Inbox should only update whenever a new letter is being added	
def updateInbox(inboxID,postForm):

	updatedInbox = ndb.Key(models.Inbox, int(inboxID)).get()
	
	#letters is essentially a list 
	updatedInbox.letters.append(ndb.Key(models.Letter, int(postForm['letterID'])))
	
	updatedInbox.put()
	return {'Success': 'Letter added to inbox'}
	
'''
Letter API functions
'''

#Returns specific letters tied to a Inbox
def getLetters(inboxID):

	letterList = [d.to_dict() for d in models.Letter.query(models.Letter.inbox == ndb.Key(models.Inbox, int(inboxID))).fetch()]
	return letterList

def getLetter(letterID):

	if ndb.Key(models.Letter, int(letterID)).get() is None:
		return {'error': 'Letter does not exist'}
	else:
		retLetter = ndb.Key(models.Letter, int(letterID)).get().to_dict()
		return retLetter
		
		
#Creates new letter 
def createLetter(postForm):
	 
	if 'title' in postForm:
		
		
		#Check to see if user already exists
		checkLetter = models.Letter.query(models.Letter.title == postForm['title']).fetch()
		if len(checkLetter) > 0:
			return {'error': 'Letter already exists'}
	
		if not postForm['title']:
			return {'error': 'Letter title can not be empty string'}
	
		
		
		newLetter = models.Letter(title=postForm['title'])
		
		newLetter.content = postForm['content']
		
		#might have to error check this 
		newLetter.inbox = ndb.Key(models.Inbox, int(postForm['inbox']))
		
		
		finalLetter = newLetter.put()
	
		
		letter_check = finalLetter.get()
		letter_check.letterID = str(finalLetter.id())
		letter_check.put()
		
		return {'New letter Registered': finalLetter.id()}
	else:
		return {'error': 'Name can not be empty string.2nd'}		

		
def deleteLetter(letterID2):
	if ndb.Key(models.Letter, int(letterID2)).get() is None:
		return {'error': 'Letter does not exist and thus can not be deleted'}
	else:
		
		#First we need to delete the referenced keyproperty items
		queryResults = models.Inbox.query(models.Inbox.letters == ndb.Key(models.Letter, int(letterID2)))
		
		for item in queryResults:
			
			pos = item.letters.index(ndb.Key(models.Letter, int(letterID2)))
			item.letters.pop(pos)
			item.put()
		
		
		#Now we delete the main attack entity
		try:
			retLetter = ndb.Key(models.Letter, int(letterID2)).get().key
			retLetter.delete()
					
		except:
			return {'error': 'error during deletion of letter'}
		
			
		return {'Success': 'Letter deleted'}


		
#All, just returns results of a query
def allUsers():
	userList = [d.to_dict() for d in models.User.query().fetch()]
	return userList
	
def allInboxes():
	inboxList = [d.to_dict() for d in models.Inbox.query().fetch()]
	return inboxList
	
def allLetters():
	letterList = [d.to_dict() for d in models.Letters.query().fetch()]
	return letterList
	
