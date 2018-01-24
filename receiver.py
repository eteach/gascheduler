import spade
import xmpp
import time
import sys

class ProducerAgent(spade.Agent.Agent):

	class ReceiveUP(spade.Behaviour.Behaviour):
		#This behaviour will receive only UPDATE_PREDICTION messages
	
		def onStart(self):
			print "Starting receiving UPDATE_PREDICTION messages . . ."

		def _process(self):
			msg = None
			msg = self._receive(True)
			if msg is not None:
				if (msg.getSubject() == "PREDICTION_UPDATE"):
					print "I got an UPDATE_PREDICTION message!"
				else:
					print "I got no UPDATE_PREDICTION message!"	
			else:
				print "I waited but got no message!"					

	def _setup(self):
		print "Producer starting . . ."

		# XMPP message generic template
		mt = spade.Behaviour.MessageTemplate(xmpp.Message()) 

		# Add the RECEIVE_UPDATE_PREDICTION behaviour
		rup = self.ReceiveUP() 
		self.addBehaviour(rup, mt)	


class ReceiverAgent(spade.Agent.Agent):
	
	class ReceiveCP(spade.Behaviour.Behaviour):
		#This behaviour will receive only CREATE_PRODUCER messages
	
		def onStart(self):
			print "Starting receiving CREATE_PRODUCER messages . . ."

		def _process(self):
			msg = None
			msg = self._receive(True)
			if msg is not None:
				if (msg.getSubject() == "CREATE_PRODUCER"):
					print "I got a CREATE_PRODUCER message!"
					#p = ProducerAgent("taskscheduler@ubuntu.local", "pv_producer", "secret")
					p = ProducerAgent("producer@ubuntu.local", "secret")
					p.start()
					#................#
					p.stop()
				else:
					print "I got no CREATE_PRODUCER message!"	
			else:
				print "I waited but got no message!"	

	class ReceiveCL(spade.Behaviour.Behaviour):
		#This behaviour will receive only CREATE_LOAD messages
	
		def onStart(self):
			print "Starting receiving CREATE_LOAD messages . . ."

		def _process(self):
			msg = None
			msg = self._receive(True)
			if msg is not None:
				if (msg.getSubject() == "LOAD"):
					print "I got a CREATE_LOAD message!"
					# ACK
					ack = xmpp.Message()
					ack.setTo(msg.getFrom())
					ack.setSubject("ACK_CL")
					self.myAgent.send(ack)
				else:
					print "I got no CREATE_LOAD message!"	
			else:
				print "I waited but got no message!"

	class ReceiveDL(spade.Behaviour.Behaviour):
		#This behaviour will receive only DELETE_LOAD messages
	
		def onStart(self):
			print "Starting receiving DELETE_LOAD messages . . ."

		def _process(self):
			msg = None
			msg = self._receive(True)
			if msg is not None:
				if (msg.getSubject() == "DELETE_LOAD"):
					print "I got a DELETE_LOAD message!"
				else:
					print "I got no DELETE_LOAD message!"	
			else:
				print "I waited but got no message!"	

	def _setup(self):
		print "Receiver starting . . ."

		# XMPP message generic template
		mt = spade.Behaviour.MessageTemplate(xmpp.Message()) 

		# Add the RECEIVE_CREATE_PRODUCER behaviour
		rcp = self.ReceiveCP() 
		self.addBehaviour(rcp, mt)

		# Add the RECEIVE_CREATE_LOAD behaviour
		rcl = self.ReceiveCL() 
		self.addBehaviour(rcl, mt)

		# Add the RECEIVE_DELETE_LOAD behaviour
		rdl = self.ReceiveDL() 
		self.addBehaviour(rdl, mt)
			

if __name__ == "__main__":
	#r = ReceiverAgent("taskscheduler@ubuntu.local", "actormanager", "secret")
	r = ReceiverAgent("taskscheduler@ubuntu.local", "secret")
	r.start()

alive = True
while alive:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        alive=False
r.stop()
sys.exit(0)
