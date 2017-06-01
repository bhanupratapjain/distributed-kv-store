# distributed-kv-store
Distributed Key Value Store

## Table of Contents

   - [distributed-kv-store](#distributed-kv-store)
      - [Setup](#setup)
      - [Monitoring Utilities](#monitoring-utilities)
      - [Design](#design)
         - [Servers](#servers)
               - [Leader](#leader)
               - [Followers](#followers)
         - [Log File](#log-file)
         - [Keystore File](#keystore-file)
         - [Load Balancer](#load-balancer)
         - [Assumptions](#assumptions)
         - [Algorithm](#algorithm)
      - [Service Registration](#service-registration)
      - [Service Discovery](#service-discovery)
      - [Network Communication](#network-communication)
      - [API Calls](#api-calls)
      - [Partition Tolerance](#partition-tolerance)
      - [Consistency](#consistency)
      - [Availability](#availability)
      - [Proposed Improvements](#proposed-improvements)
      - [Team](#team)
      
      
## Setup 
- `sudo apt-get install gcc python-dev python-pip`
- Create a virtual env with `Python 2.7`
- Go to the project root 
- Run `pip install .`
- To setup store
    -  `store addlb` : Adds the load balancer as a process.
    -  `store addsrv` : Adds a server as a process. _(Always add a load
       balancer before adding any server)_
-  To setup client and make class to the store
    - `client set` : Set a key-value to the store.
    - `client get` : Return a value w.r.t to the key specified.

## Monitoring Utilities
- `sudo apt-get install htop` - to monitor the process. 
- `ss -l -p -n | grep ",<PID>,"` - to monitor open ports of a process.

## Design

### Servers

Every server can either behave as a leader or a follower.

##### Leader
A leader is the main server with which the client interacts. There can
only be one leader at any given point in the network. Every time a
client needs to perform any `set/get` operation, it contacts the load
balancer, which returns the address of the leader. With the returned
address, the client contacts the leader for the actual operation. Other
internal tasks of the leader

- Maintain a consensus of `logs-file` and `keystore-file` on all it's
  followers.
- Notify load balancer for any dead/partitioned follower.

##### Followers

Any server that is not the leader becomes a follower. Leader contacts
all it's follower to update both `log-file` and `keystore-file`. The
idea behind followers is to provide replication of data for reliability
and take on the position of the leader if the leader dies. Hence the
system is always available as long as we have two active servers in the
network. 


### Log File
Every server maintains a `log-file` of all the `set` operations
performed on the server. A sample log entry would look like

```
Format: <index> <key> <value>
Example: 1 abc value 
```

The entire idea of maintaining the logs is to achieve consensus in an
event of partition of server failures. At every point of time, the
`log-file` of the live servers in the network should always
reflect the same data.

### Keystore File
Actual data on servers is maintained in a file stored on the disk and is
called a `keystore-file`. A sample entry in a `keystore-file` would
look like

```
Format: <key> <value>
Example: abc value 
```

At any given point the `keystore-file` on all the live servers in the
network should reflect the same data. 

### Load Balancer
There is a load balancer in our system. Every client talks to the load
balancer to get the address of the leader. Other functions of the load
balancer include

- Register a new server in the network.
- Remove a dead or partitioned server from the network.
- Heartbeat leader every t seconds, to check if's alive.
- Elect a new leader if the leader dies. 

### Assumptions
- If there is no response from the follower when the leader updates
  follower logs, then the respective follower is assumed to be dead (not network failure) and
  we remove it out of the system. To put this follower back into the
  network we have to manually restart it and register it to the load
  balancer. Once registered to the load balancer, it will sync itself to
  the leader.
- The Load Balancer is always alive.
- There is always 2 servers alive in the network. One acts as a leader
  and other as a follower. If there are less than two active servers, our
  system would be offline. 
- We are assuming that the data block in the `set` request is sanitized
  and will not contain any special characters especially '\r\n'.
- Requests are `utf-8` encoded.
- noreply in set API is ignored

### Algorithm
Our algorithm is inspired from [_The Raft Consensus
Algorithm_](https://raft.github.io/). With all the assumptions
mentioned above, the major operations include


- Whenever a new server is added, it syncs it's `log-file` with the
  leader if exists.

- With two servers registered into the network, we hold an election to
  elect a new leader. The first election is on first come first server
  basis and all the subsequent reelections are on a random basis. 

- After the leader is elected all the other servers act as followers. 

- Clients talk to the leader after getting it's address from the laod
  balancer. 

- On every `set` call on the leader, in order to achieve consensus the
  leader does two operations:
    - --Append--
        - The leader appends the set operation in it's `log-file`. 
        - The leader sends out request to all its follower to append the
          logs with the new operation.
        - If any of the follower doesn't respond with a predefined time
          frame, we assume it to be partitioned/dead. 
        - All the followers do an index check to check if there is a mismatch 
          between the last log index and last commit index. If there in an 
          index mismatch the followers contact the leader to replicate the missing
          logs and then commit all the new log entries. 
    - --Commit--
        - From the last log entry, the leader performs changes to it's data.
        - The leader requests all it's follower to do the same.
        
- When the leader dies, the load balancer holds a re-election among all
  the followers to elect a new leader. As at every point of time, there
  is a consensus on all the servers (leader and followers), thus this
  newly elected leader will have the latest `log-file` and
  `keystore-file`. If the dead leader is brought back, it has to be registered
  again with the load balancer as a server, and thus will act as a
  follower. On registration it will sync it's logs with the leader.

- When the follower dies, the leader informs the load balancer about
  this event, and the load balancer removes this server from the
  network. If this dead follower is brought back, it has to be registered again
  with the load balancer as a server. On registration it will sync it's
  logs with the leader.

## Service Registration 
Whenever there is a new server it has to register itself to the load
balancer. 

## Service Discovery 
In current implementation, service discovery is static and is done by the
load balancer which makes leader to serve every client request. There is
a lot of room for improvements here. Please check section [Proposed
Improvements](#proposed-improvements) below.

## Network Communication 
- Client - Load Balancer (server) : TCP
- Client - Leader (server): TCP
- Leader (server) - Follower (server) : UDP
- Load Balancer (server) - Leader (server) : UDP

## API Calls
    Client-LB protocol
    ------------------
    
    Request:
    get-servers\r\n
    
    Response:
    ip:port\r\n
    [more ip:port optional, but not all the servers, or LB is pointless]
    end\r\n

    Client-server protocol
    ----------------------
    
    Stripped-down memcached (get/set).
    
    Request:
    get <key>-\r\n
    
    Response:
    VALUE <key> 0 <bytes>\r\n
    <data block>\r\n
    [... more values if multiple keys requested]
    [Note: if a key is not found, there will be no VALUE for it in this list]
    END\r\n
    
    Request:
    set <key> 0 0 <bytes> [noreply]\r\n
    <data block>\r\n
    
    Response:
    STORED\r\n

## Partition Tolerance
Whenever there is a partition in the network, all followers that are
partitioned from the leader are considered to be out of the network and dead.
These servers need to register to the load balancer to come back into
the network. Once the registration is successful, these servers will
sync to the state of the leader.

## Consistency
We maintain a consensus/consistency with the leader-follower approach
inspired from RAFT. The details have been explained earlier. 

## Availability
With min. two servers active/available the system will always be
available. Availability will be impacted if the number of request are
exponential, as the the request in current implementation are redirected
to the leader.

## Proposed Improvements 

The only bottleneck in the current implementation is static service
discovery, where all the client request are redirected to the the leader
by the load balancer. We think that this can be improved by the
following strategy

- The load balancer can return any server (leader/follower) to the
  client for operation. The server can be selected either through round
  robbin or we can keep a request count for each server on the load
  balancer.
- All the `set` operations are redirected to the leader. If a follower
  gets a `set` request, it will ask the leader to take control and
  complete the operation. If a leader gets `set` then it will complete
  the operation. 
- The `get` operation can be performed by both the leader or the
  follower.
- In order to achieve consensus during `set` operation, the leader with
  broadcast a read lock to all the followers. All the subsequent read
  request on any server for that particular record will wait until the
  the read lock is released by the leader. 

## Contributing 
We love contributions from everyone. To engae, please contact [bhanupratapjain](https://github.com/bhanupratapjain) through isssues and PR

## Contributors
- [bhanupratapjain](https://github.com/bhanupratapjain)
- [sourabhb](https://github.ccs.neu.edu/sourabhb)
- [vigneshu](https://github.ccs.neu.edu/vigneshu)
