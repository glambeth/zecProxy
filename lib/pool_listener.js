var net = require('net');
var ldj = require('ldjson-stream')

exports.newPoolConnection = function poolConnection(config, miners) {
	//template strings
	var subscribeString = `{"id": 1, "method": "mining.subscribe", "params": ["${config.pool.host}", ${config.pool.port}, "poclbm-zcash/1.0", "1337"]}\n`
	var authorizeString = `{"id": 2, "method": "mining.authorize", "params": ["${config.wallet}", "x"]}\n`
	
	var poolSocket = exports.poolSocket = net.createConnection({
		port: config.pool.port,
		host: config.pool.host
	});

	poolSocket.on('connect', function(connect){
		console.log('the proxy is connected to the mining pool');
	});

	poolSocket.on('error', function(error) {
		console.log('the socket had a error: ' + error)
	});

	poolSocket.on('data', function(data) {}).pipe(ldj.parse()).on('data', function(obj) {
		console.log('====================================')
		console.log('pool socket has received data' + JSON.stringify(obj));
		if (obj.hasOwnProperty('result') || obj.method === 'mining.notify' || obj.method === 'mining.set_target') {
			//send the data to the miners
			miners.forEach(function(miner) {
				console.log('sending this to the miners' + JSON.stringify(obj));
				miner.write(JSON.stringify(obj) + '\n');
			});
		} else {
			//send the data to the mining pool
			console.log('sending the data to the mining pool');
			poolSocket.write(JSON.stringify(obj) + '\n');
		}
		console.log('====================================')
	});

	poolSocket.on('end', function() {
		console.log('the pool closed the connection, reconnecting');
		setTimeout(initiatePoolConnection(), 5000);
	});
};
