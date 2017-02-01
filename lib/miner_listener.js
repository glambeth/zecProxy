var net = require('net');
var util = require('util')
var ldj = require('ldjson-stream')

var miners = [];

exports.createMiningListener = function createMiningListener(poolConnection) {

	net.createServer(function(socket) {
		miners.push(socket);

		socket.on('data', function(data) {}).pipe(ldj.parse()).on('data', function(obj) {
			//forward data to the pool_listener to handle. 
			console.log('====================================')
			console.log('miner listener received data' + JSON.stringify(obj));
			poolConnection.write(JSON.stringify(obj) + '\n');
			console.log('this data has been sent to the mining pool')
			console.log('====================================')
		});

		socket.on('end', function() {
			console.log('miner disconnected');
			miners.splice(miners.indexOf(socket), 1);
		});

	}).listen(8000);
};

console.log('zecProxy is listening on port 8000')
exports.miners = miners;
