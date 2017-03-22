var poolListener = require('./lib/pool_listener.js');
var minerListener = require('./lib/miner_listener.js')

var poolSocket = poolListener.newPoolConnection(minerListener.miners);
minerListener.createMiningListener(poolSocket);
