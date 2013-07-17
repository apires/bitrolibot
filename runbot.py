import sys
from irc.client import ServerConnectionError
from cardreader import card_lookup

import argparse
import itertools

import irc.client
import irc.logging

target = "#hmrs"
server = "localhost"
port = 6667
nickname = "AJBot"
call_name = "!mtg"

def on_connect(connection, event):
    connection.join(target)

def on_disconnect(connection, event):
    raise SystemExit()


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('server')
    parser.add_argument('nickname')
    parser.add_argument('target', help="a nickname or channel")
    parser.add_argument('-p', '--port', default=6667, type=int)
    irc.logging.add_arguments(parser)
    return parser.parse_args()


def on_pubmsg(connection, event):
    line = event.arguments[0]
    if line.startswith(call_name):
        empty, arguments = line.split(call_name)
        card_name = arguments.strip()
        response = card_lookup(card_name)
        connection.privmsg(event.target, response)

def main():

    client = irc.client.IRC()
    try:
        c = client.server().connect(server, port, nickname)
    except irc.client.ServerConnectionError:
        print(sys.exc_info()[1])
        raise SystemExit(1)

    c.add_global_handler("welcome", on_connect)
    c.add_global_handler("disconnect", on_disconnect)
    c.add_global_handler("pubmsg", on_pubmsg)

    client.process_forever()


if __name__ == "__main__":
    main()