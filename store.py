import click
from load_balancer import LoadBalancer
import multiprocessing
import psutil
from server import Server


@click.group()
def cli():
    click.echo("Distributed Key Value Store.")


@cli.command()
@click.option('-sip', default="127.0.0.1", help='ip of server', prompt=True)
@click.option('-sport', default=6000, help='port of server', prompt=True)
@click.option('-lbport', default=5000, help='port of load balancer', prompt=True)
@click.option('-lbIp', default="127.0.0.1", help='port of load balancer', prompt=True)
def addsrv(sip, sport, lbip, lbport):
    if sip is None or sport is None or lbip is None or lbport is None:
        click.echo("Please specify valid ip and port.", err=True)
    else:
        click.echo("Adding Server @ %s:%s" % (sip, sport))
        current_process = multiprocessing.current_process()
        p = multiprocessing.Process(target=add_new_server, args=(sip, sport, lbip, lbport, current_process.pid),
                                    name='server')
        p.start()


@cli.command()
@click.option('-ip', default="127.0.0.1", help='ip of server', prompt=True)
@click.option('-port', default=6000, help='port of server', prompt=True)
def addlb(ip, port):
    if ip is None or port is None:
        click.echo("Please specify valid ip and port.", err=True)
    else:
        click.echo("Adding Load Balancer at [%s:%s]" % (ip, port))
        current_process = multiprocessing.current_process()
        p = multiprocessing.Process(target=add_new_lb, args=(ip, port, current_process.pid), name='load-balancer')
        p.start()


def add_new_server(sip, sport, lbip, lbport, ppid):
    parent_process = psutil.Process(ppid)
    parent_process.terminate()
    p = multiprocessing.current_process()
    click.echo("Starting Server with pid[%s], at [%s:%s]" % (p.pid, sip, sport))
    server = Server(sip, sport, lbip, lbport)
    server.start()


def add_new_lb(ip, port, ppid):
    parent_process = psutil.Process(ppid)
    parent_process.terminate()
    p = multiprocessing.current_process()
    click.echo("Starting Load Balancer with pid[%s], at [%s:%s]" % (p.pid, ip, port))
    lb = LoadBalancer(ip, port)
    lb.start()
