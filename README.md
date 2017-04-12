# AMQP Tester

This is a very simple AMQP tester with fail-over capabilities
useful for testing how for example a RabbitMQ cluster behaves
while stopping, starting or adding and removing nodes.

## Usage recv.py
```
usage: recv.py [-h] -u username -p password [-q queue_name]
               server [server ...]

Consume messages from AMQP queue.

positional arguments:
  server                server(s) to consume messages from

optional arguments:
  -h, --help            show this help message and exit
  -u username, --username username
                        username to use when connecting to broker
  -p password, --password password
                        password to use when connecting to broker
  -q queue_name, --queue queue_name
                        queue name to consume messages from. default: 'hello'
```

## Usage send.py
```
usage: send.py [-h] -u username -p password [-q queue_name] [-s sleep_time]
               [-m body]
               server [server ...]

Send messages to AMQP queue.

positional arguments:
  server                server(s) to consume messages from

optional arguments:
  -h, --help            show this help message and exit
  -u username, --username username
                        username to use when connecting to broker
  -p password, --password password
                        password to use when connecting to broker
  -q queue_name, --queue queue_name
                        queue name to send messages to. default: 'hello'
  -s sleep_time, --sleep-time sleep_time
                        time to sleep between sending each message
                        inmicroseconds.
  -m body, --message body
                        contents of message body
```

## Example
```
# rabbitmqctl add_user test test
Creating user "test" ...
# rabbitmqctl set_permissions -p / test ".*" ".*" ".*"
Setting permissions for user "test" in vhost "/" ...

$ ./send.py -u test -p test 10.130.236.20 10.130.236.33 10.130.236.234
Connecting to 10.130.236.20(0)...
^C
$ ./recv.py -u test -p test 10.130.236.20 10.130.236.33 10.0.236.234
Connecting to 10.130.236.20(0)...
Received #1 b'Hello, world!'
Received #2 b'Hello, world!'
Received #3 b'Hello, world!'
Received #4 b'Hello, world!'
Received #5 b'Hello, world!'
Received #6 b'Hello, world!'
Received #7 b'Hello, world!'
^C
$
```
