#Description 

This is a Stratum Proxy for Zcash using JSON-RPC written in Python Twisted. 
Originally developed for Flypool http://zcash.flypool.org/ 

**WARNING** This is still in active development. Please report any problems you encounter!

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
* implement multiple rig support
* implement failover 
* Clean up code

#Requirements
zecProxy is build with Python 2.7. The requirements for running zecProxy are:
* Python 2.7+
* python-twisted
* linux

#Installation and Start
* sudo apt-get install python-twisted
* python ./zecProxy
