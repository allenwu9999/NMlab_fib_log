# NMlab_fib_log

## How to run
- Install project dependencies
```bash
# Install protobuf compiler
$ sudo apt-get install protobuf-compiler

# Install buildtools
$ sudo apt-get install build-essential make

# Install grpc packages
$ pip3 install -r requirements.txt
```
- compile protobuf 
```bash
$ cd gRPC/
$ make
$ cd ../MQTT/
$ make
```
### 1st Terminal
- Run the gRPC backend server
```bash
$ cd gRPC/
$ python3 server.py
```
### 2nd Terminal
- Migrate database tables and run the REST backend server
```bash
$ cd REST/
$ python3 manage.py migrate
$ python3 manage.py runserver 0.0.0.0:8000
```
### 3rd Terminal
- Start the MQTT docker and run the subscriber
```bash
$ cd MQTT/
$ docker run -d -it -p 1883:1883 -v $(pwd)/mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto
$ python3 subscriber.py
```
## Using `curl` to perform client request
- Get the result of the fibonacci sequence of order n
- The following command gives the case for n = 12. (You can adjust the value to the order by yourself)
```bash
$ curl -X POST -H "Content-Type: application/json" -d '{"order" : 12}' "http://localhost:8000/rest/fibonacci"
```
- Get the reslt of the history of commands
```bash
curl "http://localhost:8000/rest/logs"
```