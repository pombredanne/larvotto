"""Implements the instant messager bot that handles communication"""

from toc import TocTalk
import larvotto.response


class MarkovBot(TocTalk):
	"""Handles all IM connection issues"""

	_resp=None

	def __init__(self,scnname,passwd,response):
		"""
		@param scnname: AIM Screen Name
		@param passwd: AIM password
		@param markov:
		"""
		assert isinstance(response,larvotto.response.BaseResponse)
		TocTalk.__init__(self,scnname,passwd)
		self._resp=response

