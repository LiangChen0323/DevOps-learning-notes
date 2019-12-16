# DevOps learning notes

This is notes of learning DevOps
16/12/19
Linux
Bash file should start with:
#!/bin/bash
\*/bin/bash can be replaced by the which bash you use
Bash file not necessarily have to have a .sh extension, it’s visually more clear that a file with .sh is a bash file.

Environment variables in scripts:
Start with “$”, use “env” to check environment variable 
Exp: $HOME in bash file

Don’t overwrite existing variables
Environment variables are should be uppercase
Exp:
FIRSTNAME = “Liang” (no space around equal sign)
Export FIRSTNAME
[Export] is a built-in command of the Bash shell. It is used to mark variables and functions to be passed to child processes. Basically, a variable will be included in child process environments without affecting other environments.
https://www.journaldev.com/28251/export-command-linux
In simple terms, environment variables are set when you open a new shell session. at any time if you change any of the variable values, the shell has no way of picking that change. The export command, on the other hand, provides the ability to update the current shell session about the change you made to the exported variable. You don’t have to wait until new shell session to use the value of the variable you changed.
https://www.geeksforgeeks.org/export-command-in-linux-with-examples/

export FIRSTNAME=”Liang” ( “” stores normal value)
export TODAYDATE=`date` (``back ticks store the results of using command date, \*run the same command again to update date value)

COMMENTS in bash scripts
Start with # sign
Exp:
#COMMENTS

Docker

In docker-compose file
“Build .” build from DockerFile in current location

Swarm Mode
A server clustering service

To check swarm is active or not: docker swarm | grep Swarm
By default, swarm is inactive, to active swarm: docker swarm init (create a manager node)
Create a new service:
docker service create [OPTIONS] IMAGE [COMMAND][arg...]
Exp:
docker service create alpine (creates 1 alpine replica)

ID NAME MODE REPLICAS IMAGE PORTS
mjfnz592fd8g awesome_bohr replicated 1/1 alpine:latest

Usage: docker update [OPTIONS] CONTAINER [CONTAINER...]

Update configuration of one or more containers

Usage: docker service update [OPTIONS] SERVICE

Update a service

When one of the containers failed, Swarm will automatically start a new container.

Steps:

1. docker swarm init --advertise-addr 192.168.0.48(current manager node IP) on manager node
2. docker swarm join --token SWMTKN-1-0v9wupgq9ni1m0t9y83b8g0xo9vz3g7ntoune0w6ldo5bcf93k-4zdxl7xqxmlb87xbk7nydawb9 192.168.0.48:2377 (Join swarm as a worker) on worker node
3. docker node ls(check node list)
4. Change a worker to Manager node:
   a. docker node update –role manager xxx(node name)
   b. docker swarm join-token manager(manage node) to get command for changing worker node to manager node(worker node)
5. docker service create --replicas 3 alpine ping 8.8.8.8 (create service(with 3 replicas) on manager node)

- docker node
- docker swarm
- docker service

what’s the relation between node, swarm and service?
A node is an instance of the Docker engine participating in the swarm.
A node is an instance of the Docker engine participating in the swarm.
A task is a running container which is part of a swarm service and managed by a swarm manager, as opposed to a standalone container.
A service is the definition of the tasks to execute on the manager or worker nodes. It is the central structure of the swarm system and the primary root of user interaction with the swarm. When you create a service, you specify which container image to use and which commands to execute inside running containers. In the replicated services model, the swarm manager distributes a specific number of replica tasks among the nodes based upon the scale you set in the desired state.

https://docs.docker.com/engine/swarm/key-concepts/

swarm mode that enables you to create a cluster of one or more Docker Engines called a swarm. A swarm consists of one or more nodes.
https://docs.docker.com/engine/swarm/how-swarm-mode-works/nodes/

What’s the difference between a work node and a manager node?
To deploy your application to a swarm, you submit a service definition to a manager node. The manager node dispatches units of work called tasks to worker nodes. Manager nodes also perform the orchestration and cluster management functions required to maintain the desired state of the swarm. Manager nodes elect a single leader to conduct orchestration tasks. Worker nodes receive and execute tasks dispatched from manager nodes. By default, manager nodes also run services as worker nodes, but you can configure them to run manager tasks exclusively and be manager-only nodes.
https://docs.docker.com/engine/swarm/key-concepts/