import pyHook 
import pygame
import sys 
import random

class rawr(): 
	def __init__(self, quitStr="hobgoblin", sleepStr="derp", dropKeysFlag=True, slowMouseFlag=True, mouseLockStr="."):
		# default settings built into class declaration
		self.hm = pyHook.HookManager() # input hook manager
		self.hm.KeyDown = self.OnKeyboardEvent  # key down events
		self.hm.MouseAll = self.OnMouseEvent # mouse events
		self.hm.HookMouse() # hook mouse
		self.hm.HookKeyboard() # hook keyboard
		
		# setting variables
		self.quitStr = quitStr
		self.sleepStr = sleepStr
		self.dropKeysFlag = dropKeysFlag
		self.slowMouseFlag = slowMouseFlag
		self.mouseLockStr = mouseLockStr
		# buffer
		self.lastChars = []
		
		# set the buffer to the maximum size needed
		for t in range(0, max(len(self.quitStr), len(self.sleepStr), len(self.mouseLockStr))):
			self.lastChars.append('\x00')
		
		# state variables
		self.dropKeyCount = random.randint(0,5)
		self.mouseLockCount = random.randint(0,5)
		self.mouseLockout = 0
		self.tempSleep = 0
		self.startup = True
		
	def run(self):
	# initialize pygame and start the game loop 
		pygame.init() 
		while True: 
			pygame.event.wait()
	
	def typed(self, s):
		slength = len(s) # string length
		blength = len(self.lastChars) # buffer length
		if ''.join(self.lastChars[blength-slength:]) == s: # check if strings match (only check for valid lengths)
			return True
		else:
			return False
	
	def OnKeyboardEvent(self, event):
		# save the last typed characters into buffer for detecting combinations
		self.lastChars.append(chr(event.Ascii))
		self.lastChars.pop(0)
		
		# delay start
		if self.startup:
			self.tempSleep = event.Time #+ 300000 # don't start for 5 minutes
			self.startup = False
		
		# check for quit string
		if self.typed(self.quitStr):
			sys.exit() # quit
		
		# check for sleep string
		if self.typed(self.sleepStr):
			self.tempSleep = event.Time + 120000 # if sleep string, stop for 2 minutes
		
		# if sleeping, pass the event
		if event.Time < self.tempSleep:
			return True
		# if mouse lock string is set, process that
		if self.mouseLockStr is False:
			pass
		elif self.typed(self.mouseLockStr):
			# typed mouse lock string
			# time to execute?
			if self.mouseLockCount > 10:
				# lock the mouse for 5 seconds, reset the counter to between 0 and 5 for randomness
				self.mouseLockout = event.Time + 5000
				self.mouseLockCount = random.randint(0,5)
			else:
				# not yet, increment count
				self.mouseLockCount += 1
		
		# if drop keys flag is set, process that
		if self.dropKeysFlag is False:
			# not dropping keys, pass event
			return True
		# time to execute?
		elif self.dropKeyCount > 25:
			# reset the count to between 0 and 5
			self.dropKeyCount = random.randint(0,5)
			# drop the key
			print "drop"
			return False
		else:
			# not yet, increment count
			self.dropKeyCount += 1
			return True
			
	def OnMouseEvent(self, event):
		# if sleeping, pass event
		if event.Time < self.tempSleep:
			return True
		# slowing the mouse?
		elif self.slowMouseFlag:
			# change modulus to increase mouse "issues"
			# modulus of 2 makes mouse borderline unusable 
			if event.Time % 10 == 0: 
				return False
		# mouse locked, drop event
		if event.Time < self.mouseLockout:
			return False
		
		# default
		return True

	
if __name__ == "__main__":
	if len(sys.argv) == 6:
		# did they provide custom args?
		k = rawr(quitStr=sys.argv[1], sleepStr=sys.argv[2], dropKeysFlag=sys.argv[3], slowMouseFlag=sys.argv[4], mouseLockStr=sys.argv[5])
	else:
		# use defaults
		 k = rawr()
	# And here...we.......go
	k.run()
