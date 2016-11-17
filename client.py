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
        sock.send("set " + key + " 0 0 " + str(len(value)) + "\r\n"+value+"\r\n")
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
@click.argument("ip")
@click.argument("port")
@click.argument("key")
@click.argument("value")
def set(ip, port, key, value):
    client = Client()
    server = client.get_server(ip, int(port))
    result = client.set(key,value,server[0],int(server[1]))
    if result:
        click.echo("Success")
    else:
        click.echo("Error")


@cli.command()
@click.argument("ip")
@click.argument("port")
@click.argument('keys', nargs=-1, required=True)
def get(ip, port, keys):
    client = Client()
    server = client.get_server(ip, int(port))
    response = client.get(keys, server[0], int(server[1]))
    parsed = ProtoParser.parse_get_response(response)

    for k, v in parsed.iteritems():
        click.echo(str(k) + " " + str(v))


if __name__ == "__main__":
    cli()
