var poolListener = require('./lib/pool_listener.js');
var minerListener = require('./lib/miner_listener.js')

poolListener.newPoolConnection(minerListener.miners);
minerListener.createMiningListener(poolListener.poolSocket);
