#Description 

This is a Stratum Proxy for Zcash using JSON-RPC written in Javascript. 
Originally developed for Flypool http://zcash.flypool.org/ 

**WARNING** This is still in active development. Please report any problems you encounter, and use with caution! 

#How it Works
```
   Pool A <---+                        +-------------+ Rig1 / PC1
 (Active)      |                       |
               |                       +-------------+ Rig2 / PC2
               |                       |
  Pool B <---+-----StratumProxy  <-----+-------------+ Rig3 / PC3
(FailOver)                             |
                                       +-------------+ Rig4 / PC4                                      
```

#Todo
* implement failover 
* Clean up code
* Setup Logging

#Requirements
zecProxy is build with nodeJS. The requirements for running zecProxy are:
* nodeJS
* npm
* linux

#Installation and Start
* git clone https://github.com/glambeth/zecProxy.git
* cd zecProxy
* npm install
* node proxy.js

See config.json to change settings. 
The proxy will automatically listen on port 8000 for miners

