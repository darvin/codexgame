# -*- coding:utf-8 -*-

#from codewars.settings import PATH_TO_RUN, SCP_EXEC_PATH, SSH_EXEC_PATH
#from codewars.engine.parser import parse
from commandparser import parse

import sys, threading

# =======================================================

class BotError(Exception):
	"""Base class for exceptions in this module."""
	pass

class BotWaitError(BotError):
	"""Exception raised for errors when wait input form bot.

	Attributes:
		bot -- bot which raise exception
	"""

	def __init__(self, bot):
		self.bot = bot

class BotInputError(BotError):
	"""Exception raised for errors in input form bot.

	Attributes:
		bot -- bot which raise exception
	"""

	def __init__(self, bot):
		self.bot = bot

# -----------------------------

class CommonBot(object):
	"""
	Class to communicate with players-programs
	"""
	def __init__(self, botid, botexe, sship="", sshuser="", ssh=True):
		"""
		botid, botexe - bot id and bot exe file
		sship, sshuser - sship and ssh username
		ssh - run by ssh?
		"""
		self.botid, self.botexe, self.sship, self.sshuser, self.ssh = \
				botid, botexe, sship, sshuser, ssh

	def connect(self):
		"""
		Starts player-programm instance
		"""
		if self.ssh:
			sshaddress = '%s@%s' % (self.sshuser, self.sship)
			sys.command("%s %s %s:%s" % \
				(SCP_EXEC_PATH, self.botexe, sshaddress, PATH_TO_RUN) )
			sys.command("%s %s 'chmod +x %s'" % (SSH_EXEC_PATH, sshaddress, PATH_TO_RUN))
			sshargs = "'%s'" % PATH_TO_RUN
			self.__proc = subprocess.Popen(executable=SSH_EXEC_PATH, \
					args=sshargs, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
		else:
			self.__proc = subprocess.Popen(self.botexe, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

	def send(self, sendstring):
		"""
		Sends line to program
		"""
		self.__proc.stdin.write(sendstring+'\n')

	def recieve(self, timeout=5):
		"""
		Reads line from programm output, stripes \\n, timeout is timeout, default 5
		"""
		f  = select.select( [self.__proc.stdout], [], [], timeout)
		ff = f[0]
		try:
			fff = ff.pop()
		except IndexError:
			raise BotWaitError
		return fff.readline()

	def disconnect(self):
		"""
		Terminates programm
		"""
		self.__proc.terminate()

# =======================================================

class CommonEngine(object):
	"""
	Parent class for engines class's
	"""

	def __init__(self, bots, opts=""):
		"""
		bots - list of bots
		opts - some custom options to engine, dict
		"""
		self.opts  = opts
		self.bots = bots

	def start_game(self):
		"""
		Stops all players-games 
		"""
		for bot in self.bots:
			bot.connect()

	def stop_game(self):
		"""
		Stops all players-games 
		"""
		for bot in self.bots:
			bots.disconnect()

	#def recieve_all(self):
	#	"""
	#	Recieve from all bots and returns dict
	#	"""
	#	recieved = {}
	#	for bot in self.bots:
	#		recieved[bot.id] = bot.recieve()
	#	return recieved
	
	#def send_all_st(self, st):
	#	"""
	#	Send to all bots string st
	#	"""
	#	for bot in self.bots:
	#		bot.send(st)

	#def send_all(self, senddict):
	#	"""
	#	Send to all bots
	#	senddict - dict "player id": "string to send"
	#	"""
	#	for bot in senddict:
	#		bot.send(senddict[botname])
	
	def start(self):
		"""
		main loop
		"""
		self.start_game()
		while True:
			self.main()
		self.stop_game()
	
	def main(self):
		"""
		example main function
		"""
		recieved = self.recieve_all()
		self.send_all(recieved)
		self.send_all_st("Now exit!")
		return False #Exit!

# =======================================================

class ParseError(Exception):
	pass

class UnaccessibleProperty(Exception):
	pass

class TwoTransitionProperty(Exception):
	pass

# -----------------------------

class CourseTransition(Exception):
	pass

# -----------------------------

class ParseBot(CommonBot):
	
	accessible = True
	__botObjects = []
	
	def test(self, v='test ok'):
		print 'test>', v
		return v
	
	test.accessible = True
	test.transition = True
	
	def replyer(self):
		while 1:
			try:
				self.send(self.parser(self.recieve()))
			except (ParseError, IndexError), e:
				self.send('!ERROR: %s' % e)
			except CourseTransition:
				return
	
	def parser(self, s):
		
		def parseParam(v):
			if type(v) == str:
				return eval(v) # А-а-а-а!!
			else:
				n = v.getName()
				if n == 'object':
					obj = self.__botObjects[int(v[1])]
					if type(obj).__name__ != v[0]:
						raise UnaccessibleProperty(v)
					return obj
				elif n == 'list':
					return parseList(v)
		
		def parseList(v):
			return [ parseParam(x) for x in v ]
		
		obj = None
		course = False
		for x in parse(str(s)):
			
			n = x.getName()
			
			if obj == 0:
				if x[0] == 'self':
					obj = self
				else:
					obj = globals()[x[0]]
			elif n == 'ident':
				obj = obj.__getattribute__(x[0])
			elif n == 'get':
				obj = obj.__getitem__(*parseList(x))
			elif n == 'exec':
				obj = obj(*parseList(x))
			
			if not (type(obj) == str or type(obj) == int or ('accessible' in dir(obj) and obj.accessible)):
				raise UnaccessibleProperty(x)
			
			if 'transition' in dir(obj) and obj.transition:
				if course:
					raise TwoTransitionProperty()
				course = True
		
		if course:
			raise CourseTransition()
		
		if type(obj) == str:
			return '"%s"' % obj
		elif type(obj) == int:
			return str(obj)
		else:
			self.__botObjects.append(obj)
			return '<%s %d>' % (type(obj).__name__, len(self.__botObjects)-1)

v = ParseBot(0, 0)
print v.parser('self.test(1901)')

# =======================================================

class ParseEngine(CommonEngine):
	
	pass
	














