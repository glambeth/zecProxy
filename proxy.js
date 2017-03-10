var poolListener = require('./lib/pool_listener.js');
var config = require('./config.json')
var minerListener = require('./lib/miner_listener.js')

poolListener.newPoolConnection(config, minerListener.miners);
minerListener.createMiningListener(poolListener.poolSocket);
