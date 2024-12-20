# Users distributed database using Chord

## Distributed Systems Course 2024 - UNRC

*D'Autilio Joel - Rossi Pablo*
    
This project was developed as the final project for the *Telecomunications and Distributed Systems* Course at Universidad Nacional de Río Cuarto, Argentina.

The [Chord](https://en.wikipedia.org/wiki/Chord_(peer-to-peer)) algorithm is designed to provide efficient and scalable key-value lookups in decentralized environments.
It utilizes a distributed hash table (DHT) to distribute data uniformly across nodes, ensuring balance and scalability.
Chord works well for dynamic networks where nodes may frequently join or leave.

In this project, we apply the Chord alogorithm to implement a distributed users database. The system handles a set of Users, and each node contains a subset of it. A node can fetch a user's information (from it's own table or from one if its peers), or it can insert/update an user.

This implementation also supports fault tolerance, ensuring the system remains operational and no information is lost even if a number of nodes fail.


## Install and run

To install the project, it's recommended to first create a virtual environment for python. For example, one can be created and activated using `venv` with the following commands:

    python -m venv .env
    source .env/bin/activate

After that, the dependencies can be installed with the following:

    pip install -r requirements.txt

Once the dependencies are installed, the `peer.app` script can be used to launch an HTTP server along with a GRPC server. The arguments can be found with this command;

    python -m peer.app -h

### Example

This command runs the HTTP server with port 5000 and the GRPC server with port 50051, both in `localhost`.

    python -m peer.app -p 50051 -P 5000

To join to an existing ring, to a chord node also in `localhost`, the following command can be used.

    python -m peer.app -p 50052 -P 5002 -j 50051

If the target chord node to join to is in a different machine with ip `<join-ip>`, use this command.

    python -m peer.app -a <my-ip> -p <chord-port> -P <http-port> -J <join-ip> -j <join-port>

### Add users

Once the ring is stablished, the `setusers` script can be used to add multiple users to the system. For example, to add 10 users through a node in this machine with port 5000, use the following command:

    setusers -n 10 -p 5000

The Users table in a local node are displayed in `output/<port>/users.txt`.
In the same directory, the `log.txt` file displays the chord node's log, and `finger.txt` contains internal information (ID, predecessor, finger table).

## Project Structure

The chord server implementation can be found under `peer/`.
Inside it, `chord/` and `users/` contain the code for the GRPC `chord` and `users` servicers.
The former focuses on the infrastructure for the server, handling node joins, leaves, finding and stabilization processes. The later acts as a database manager, handling the addition, removal and transference of users.

The `proto/` directory contains the protobuf definitions for the remote call procedures (RCP) used by both servicers. The code generated by GRPC is placed under `stubs/`.

The `peer/server.py` file contains the `Server` class, implementing a GRPC server which uses both servicers previously mentioned.
The `peer/app.py` script launches a GRPC server along with an HTTP server, exposing two endpoints (`GET` and `POST`) to fetch and insert users.

    .
    │   constants.py
    ├───peer
    │   │   address.py
    │   │   app.py
    │   │   server.py
    │   ├───chord
    │   │       chord_servicer.py
    │   │       node.py
    │   │       remote.py
    │   │       utils.py
    │   └───users
    │           remote.py
    │           users_servicer.py
    │           utils.py
    ├───proto
    │       chord.proto
    │       users.proto
    └───stubs
            ...

The following diagram visualises the implementation of a peer node.

![peer](/docs/assets/images/peer.svg)
