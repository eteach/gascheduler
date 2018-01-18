import spade
import xmpp
import time
import sys

class MyAgent(spade.Agent.Agent):
	
	class Rec_CPbehav(spade.Behaviour.Behaviour):
		#This behaviour will receive only CREATE_PRODUCER messages
	
		def onStart(self):
			print "Starting receiving . . ."

		def _process(self):
			msg = None
			
			# Blocking receive for 10 seconds
			msg = self._receive(True)
			# Blocking receive
			#self.msg = self._receive(True)
			# Non blocking receive
			#self.msg = self._receive(False)
			
			# Check wether the message arrived
			if msg is not None:
				print "I got a message!"
				if (msg.getSubject() == "CREATE_PRODUCER"):
					print "I got a CREATE_PRODUCER message!"
				else:
					print "I got no CREATE_PRODUCER message!"
					
			else:
				print "I waited but got no message!"				

	def _setup(self):
		print "MyAgent starting . . ."

		# Add the RECEIVE_CREATE_PRODUCER behaviour
		rcp = self.Rec_CPbehav() 
		mt1 = spade.Behaviour.MessageTemplate(xmpp.Message())
		self.addBehaviour(rcp, mt1)				

if __name__ == "__main__":
	a = MyAgent("receiver@r7.local", "secret")
	a.start()

alive = True
while alive:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        alive=False
a.stop()
sys.exit(0)
