"""Implements the instant messager bot that handles communication"""




import warnings

#Twisted warns as it's claiming to be re-writing
#twistied.words.im at some point soon, it has been doing so
#for several 
warnings.filterwarnings("ignore",module="twisted.words.im")
import twisted.words.im.tocsupport as ts
warnings.resetwarnings()

#Indirect warning as 'oscar' imports md5 which
#is deprecated in Python v2.6
warnings.filterwarnings("ignore",module="twisted.words.protocols",category=DeprecationWarning)
from twisted.words.protocols import oscar
warnings.resetwarnings()

from twisted.internet import reactor, protocol
import larvotto.response
import time

class MarkovBot(oscar.BOSConnection):
	"""
	Handles all IM connection and event issues
	Also, twisted is lame and won't give you access to the object that it
	constructs, this is why the __call__ method is override to simulate a
	constructor
	"""

	capabilities = [oscar.CAP_CHAT]
	_resp=None

	def __init__(self,response):
		assert isinstance(response,larvotto.response.BaseResponse)
		self._resp=response

	def __call__(self,*args,**kwargs):
		oscar.BOSConnection.__init__(self,*args,**kwargs)
		return self

	def receiveMessage(self, user, multiparts, flags):
		self.sendMessage(user.name, self._resp.get(user.name,multiparts))

	def initDone(self):
		self.requestSelfInfo().addCallback(self.gotSelfInfo)
		self.requestSSI().addCallback(self.gotBuddyList)

	def gotSelfInfo(self, user):
		self.name = user.name

	def gotBuddyList(self, l):
		self.activateSSI()
		self.setProfile("LarvottoBot for %s"%self.name)
		self.setIdleTime(0)
		self.clientReady()


def Start(ScreenName,Passwd,ResponseObj):
	"""Starts the bot"""
	class OA(oscar.OscarAuthenticator):
	   BOSClass = MarkovBot(ResponseObj)

	protocol.ClientCreator(reactor, OA, ScreenName, Passwd, icq=0).connectTCP('login.oscar.aol.com', 5190)
	reactor.run()


