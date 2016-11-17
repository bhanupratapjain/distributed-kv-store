import socket

import click

import constants
from request_parser import ProtoParser


class Client:
    def get(self, keys, sip, sport):
        sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((sip, sport))
        msg = "get "
        for key in keys[:-1]:
            msg += str(key) + " "
        msg += str(keys[-1]) + "\r\n"
        sock.send(msg)
        tmsg = ""
        while True:
            pmsg = sock.recv(constants.BUFFER_SIZE)
            if len(pmsg) == 0:
                break
            tmsg += pmsg

        sock.close()
        return tmsg

    def set(self, key, value, sip, sport):
        sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((sip, sport))
        sock.send("set " + key + " 0 0 " + str(len(value)) + "\r\n" + value + "\r\n")
        msg = sock.recv(constants.BUFFER_SIZE)
        sock.close()
        if msg == "STORED\r\n":
            return True
        else:
            return False

    def get_server(self, sip, sport):
        sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((sip, sport))
        sock.send("get-servers")
        msg = sock.recv(constants.BUFFER_SIZE)
        # print msg
        sock.close()
        return ProtoParser.parse_srv_addr(msg)


@click.group()
def cli():
    pass


@cli.command()
@click.option("-lbip", default="127.0.0.1", prompt=True, required=True)
@click.option("-lbport", default=5002, prompt=True, required=True)
@click.option("-key", prompt=True, required=True)
@click.option("-value", prompt=True, required=True)
def set(lbip, lbport, key, value):
    client = Client()
    server = client.get_server(lbip, int(lbport))
    result = client.set(key, value, server[0], int(server[1]))
    if result:
        click.echo("Success")
    else:
        click.echo("Error")


@cli.command()
@click.option("-lbip", default="127.0.0.1", prompt=True, required=True)
@click.option("-lbport", default=5002, prompt=True, required=True)
@click.option('-keys', required=True, prompt=True)
def get(lbip, lbport, keys):
    client = Client()
    server = client.get_server(lbip, int(lbport))
    response = client.get(keys, server[0], int(server[1]))
    parsed = ProtoParser.parse_get_response(response)

    for k, v in parsed.iteritems():
        click.echo(str(k) + " " + str(v))


if __name__ == "__main__":
    cli()
