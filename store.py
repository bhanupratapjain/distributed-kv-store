import click
from load_balancer import LoadBalancer
import multiprocessing
import psutil


@click.group()
def cli():
    click.echo("Distributed Key Value Store.")


@cli.command()
@click.option('-ip', help='ip of the server', prompt=True)
@click.option('-port', help='port of the server', prompt=True)
def addsrv(ip, port):
    if ip is None or port is None:
        click.echo("Please specify valid ip and port.", err=True)
    else:
        click.echo("Adding server @ %s:%s" % (ip, port))


@cli.command()
@click.option('-ip', default="127.0.0.1", help='ip of load balancer', prompt=True)
@click.option('-port', default=5000, help='port of load balancer', prompt=True)
def addlb(ip, port):
    if ip is None or port is None:
        click.echo("Please specify valid ip and port.", err=True)
    else:
        click.echo("Adding Load Balancer at [%s:%s]" % (ip, port))
        current_process = multiprocessing.current_process()
        p = multiprocessing.Process(target=add_new_lb, args=(ip, port, current_process.pid), name='daemon')
        p.start()


def add_new_lb(ip, port, ppid):
    parent_process = psutil.Process(ppid)
    parent_process.terminate()
    p = multiprocessing.current_process()
    click.echo("Starting Load Balancer with pid[%s], at [%s:%s]" % (p.pid, ip, port))
    lb = LoadBalancer(ip, port)
    lb.start()
