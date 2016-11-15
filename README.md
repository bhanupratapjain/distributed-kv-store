# distributed-kv-store
Distributed Key Value Store

## Setup 
- `sudo apt-get install gcc python-dev python-pip`
- create a virtual env with `Python 2.7`
- go to the project root 
- run `pip install --editable .`
- pip install portalocker # locks across multiple platforms
## Monitor Utilities
- `sudo apt-get install htop` - to monitor the process. 
- `ss -l -p -n | grep ",<PID>,"` - to monitor open ports of a process.


## TO DO
- Save to Files
- Implement Memcached
- Implement Master
- Multi Thread Server
- Exception Handling in Server and Client
- Server - Server Communication

## Design Strategy


## Team
- [bhanupratapjain](https://github.ccs.neu.edu/bhanupratapjain)
- [sourabhb](https://github.ccs.neu.edu/sourabhb)
- [vignushu](https://github.ccs.neu.edu/vignushu)