from twisted.internet.protocol import Factory
from twisted.internet import reactor, protocol
import json
import re

'''
Current Problems/Thoughts/Things to do:
	1) Use deferreds..saves a lot of time. 
	2) global variables (this should be fixed with deferreds though)
'''



miners = []
miningPool = None
curJon = None
Target = None
IdToMiner = {}

class StratumProtocol(protocol.Protocol):
	def __init__(self, factory):
		self.factory = factory
		#this is not sent to 5 to avoid collisions with responses to other stratum procedures
		self.reqID = 5

	#this function also inserts connections to IdToMiner
	#todo: refactor and fix the side effect in this fuction
	def incrementID(self, json_data):
		json_data['id'] = self.reqID
		lineNew = json.dumps(json_data, sort_keys=True)
		sep = '['
		rest = sep + lineNew.split(sep, 1)[1]
		beg = lineNew.split(sep, 1)[0]
		rest = re.sub(r'\s+', '', rest)
		newString = beg + rest + '\n'
		IdToMiner[self.reqID] = self
		self.reqID = self.reqID + 1
		return newString

	def handleMinerLine(self, line):
		#BE CAREFUL OF NOT HAVING /n at the end of a string
		global curJob
		global target
		json_data = json.loads(line)
		print 'sending data to pool'
		if json_data['method'] == 'mining.submit':
			miningPool.transport.write(self.incrementID(json_data))
		else:
			miningPool.transport.write(line + '\n')

	def handlePoolLine(self, line):
		json_data = json.loads(line)
		reqID = json_data['id']
		if reqID in IdToMiner:
			IdToMiner[reqID].transport.write(line)
			IdToMiner.pop(reqID)
			return
 		for miner in miners:
			print 'sending data to miner'
			miner.transport.write(line)

	def connectionMade(self):
		print '=================================================='
		print 'Connection Made Function in StratumProtocol'
		global miningPool
		if self.factory.__class__ == StratumMinerFactory:
			miners.append(self)
			print 'miner connection made'
		if self.factory.__class__ == StratumPoolFactory:
			miningPool = self
			print 'mining pool connection made'
		print '=================================================='

	def connectionLost(self, reason):
		print '=================================================='
		print 'Connection Lost'
		if self.factory.__class__ == StratumMinerFactory:
			miners.remove(self)
			print 'the connection was from a miner'
		else:
			print 'the connection was from the pool'
			print 'trying to reconnect to pool'
			reactor.connectTCP("us1-zcash.flypool.org", 3333, StratumPoolFactory())
		print '=================================================='

	def dataReceived(self, data):
		print '=================================================='
		print 'Data Received'
		print data
		if self.factory.__class__ == StratumMinerFactory:
			#received data from miner. Send to the pool
			print ' the data is from the miner'
			if "\n" in data:
				for line in data.splitlines():
					self.handleMinerLine(line)
			else:
				self.handleMinerLine(data) 

		elif self.factory.__class__ == StratumPoolFactory:
			#received data from pool. Send to miner
			#currently the data is sent to all of the miners, but instead
			#it should only be sent 
			print ' the data is from the pool'
			if "\n" in data:
				for line in data.splitlines():
					self.handlePoolLine(line)
			else:
				self.handlePoolLine(data) 
		print '=================================================='

class StratumPoolFactory(protocol.ClientFactory):
	def __init__(self):
		print '=================================================='
		print 'inside StraumFactory init'
		print '=================================================='
		return

	def buildProtocol(self, addr):
		print '=================================================='
		print 'inside StraumFactory buildProtocol'
		print '=================================================='
		return StratumProtocol(self)

	def clientConnectionFailed(self, connector, reason):
		print '=================================================='
		print 'inside StraumFactory clientConnectionFailed'
		print reason
		print '=================================================='

	def clientConnectionLost(self, connector, reason):
		print '=================================================='
		print 'inside StraumFactory clientConnectionLost'
		print reason
		print '=================================================='

class StratumMinerFactory(protocol.Factory):
	def __init__(Self):
		return

	def buildProtocol(self, addr):
		return StratumProtocol(self)

	def clientConnectionFailed(self, connector, reason):
		print '=================================================='
		print 'inside StraumMinerFactory clientConnectionFailed'
		print reason
		print '=================================================='

	def clientConnectionLost(self, connector, reason):
		print '=================================================='
		print 'inside StraumMinerFactory clientConnectionLost'
		print reason
		print '=================================================='

reactor.connectTCP("us1-zcash.flypool.org", 3333, StratumPoolFactory())
reactor.listenTCP(3334, StratumMinerFactory())
reactor.run()
