import spade
import xmpp
import time
import sys

class MyAgent(spade.Agent.Agent):
	class CP_behav(spade.Behaviour.OneShotBehaviour):

		def _process(self):
			# First, form the receiver AID
			#receiver = spade.AID.aid(name="receiver@ubuntu.local", addresses=["xmpp://receiver@ubuntu.local"])
			
			# Second, build the message
			# XMPP message
			msg = xmpp.Message()
			msg.setTo("receiver@r7.local")
			msg.setSubject("CREATE_PRODUCER")
			msg.setBody("CREATE_PRODUCER BODY")
			
			# Third, send the message with the "send" method of the agent
			self.myAgent.send(msg)
			print "I send a CREATE_PRODUCER message!"

	def _setup(self):
		print "MyAgent starting . . ."
		cpb = self.CP_behav()
		self.addBehaviour(cpb, None)

if __name__ == "__main__":
	a = MyAgent("sender@r7.local", "secret")
	a.start()

alive = True
while alive:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        alive=False
a.stop()
sys.exit(0)
