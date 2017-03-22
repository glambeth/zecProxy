var config = require('../config.json')
var net = require('net');
var ldj = require('ldjson-stream')


exports.newPoolConnection = function poolConnection(miners) {

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
		if (obj.method === 'mining.notify' || obj.method === 'mining.set_target') {
			//send the data to all the miners
			miners.forEach(function(value,key) {
				console.log('sending this to the miners' + JSON.stringify(obj));
				value.write(JSON.stringify(obj) + '\n');
			});
		} else {
			//forward the data only to the correct miner
			miners.get(obj.id).write(JSON.stringify(obj) + '\n');
		}
		console.log('====================================')
	});

	poolSocket.on('end', function() {
		console.log('the pool closed the connection');
	});
};


//idea creat an 