from google.appengine.ext import ndb



''' User is the main entity model''' 


'''A user can have only one class but a class can be taken by multiple users - Many to one '''
'''A class has multiple attacks but attacks are locked into a class -   Many to one'''

class Inbox(ndb.Model):
	inboxID = ndb.StringProperty()
	name = ndb.StringProperty()
	letters = ndb.KeyProperty(kind='Letter', repeated=True)
	user = ndb.KeyProperty(kind='User', repeated=False)
	
	'''OSU CS496 - Code is from lecture: Justin Wolford'''
	def to_dict(self):
		d = super(Inbox, self).to_dict()
		d['letters'] = [r.id() for r in d['letters']]
		d['user'] = str(d['user'])
		return d
		
		
		
class User(ndb.Model):
	userID = ndb.StringProperty()
	name = ndb.StringProperty()
	password = ndb.StringProperty()
	date_created = ndb.DateProperty()
	latitude = ndb.StringProperty()		#we are going to store last known lattitude
	longitude = ndb.StringProperty()	#we are going to store last known longitude
	
	'''OSU CS496 - Code is from lecture: Justin Wolford'''
	def to_dict(self):
		d = super(User, self).to_dict()
		d['date_created'] = str(d['date_created'])
		return d
	

class Letter(ndb.Model):
	title = ndb.StringProperty()
	content = ndb.StringProperty()
	letterID = ndb.StringProperty()
	inbox = ndb.KeyProperty(kind='Inbox', repeated=False)
	
	
	def to_dict(self):
		d = super(Letter, self).to_dict()
		d['inbox'] = str(d['inbox'])
		return d