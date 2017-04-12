#!/usr/bin/env python3
#
# Copyright 2017 Frode Nordahl
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import pika
import time

parser = argparse.ArgumentParser(
            description='Send messages to AMQP queue.')
parser.add_argument('servers', metavar='server', type=str, nargs='+',
                    help='server(s) to consume messages from')
parser.add_argument('-u', '--username', metavar='username', type=str,
                    required=True,
                    help='username to use when connecting to broker')
parser.add_argument('-p', '--password', metavar='password', type=str,
                    required=True,
                    help='password to use when connecting to broker')
parser.add_argument('-q', '--queue', metavar='queue_name', type=str,
                    default='hello',
                    help="queue name to send messages to."
                         " default: 'hello'")
parser.add_argument('-s', '--sleep-time', metavar='sleep_time', type=int,
                    default=50000,
                    help='time to sleep between sending each message in'
                         'microseconds.')
parser.add_argument('-m', '--message', metavar='body', type=str,
                    default='Hello, world!',
                    help='contents of message body')
args = parser.parse_args()

server_list = args.servers
last_server = None


def connect():
    global last_server, server_list
    if last_server is None:
        last_server = 0
    else:
        last_server = last_server + 1
    if last_server > len(server_list) - 1:
        last_server = 0
    server = server_list[last_server]
    print('Connecting to {}({})...'.format(server, last_server))
    creds = pika.PlainCredentials(args.username, args.password)
    connparams = pika.ConnectionParameters(server, credentials=creds)

    connection = pika.BlockingConnection(connparams)
    channel = connection.channel()
    channel.queue_declare(queue=args.queue)
    return (connection, channel)


(connection, channel) = connect()
while True:
    try:
        channel.basic_publish(exchange='',
                              routing_key=args.queue,
                              body=args.message)
        time.sleep(args.sleep_time/1000000.0)
    except KeyboardInterrupt:
        break
    except pika.exceptions.ConnectionClosed:
        print('Connection closed, reconnecting...')
        (connection, channel) = connect()
        pass
connection.close()
