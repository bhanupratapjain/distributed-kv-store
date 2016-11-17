import click
from load_balancer import LoadBalancer
import multiprocessing
from server import Server


@click.group()
def cli():
    click.echo("Distributed Key Value Store.")


@cli.command()
@click.option('-cip', default="127.0.0.1", help='client ip of server', prompt=True)
@click.option('-cport', default=7001, help='client port of server', prompt=True)
@click.option('-sip', default="127.0.0.1", help='server ip of server', prompt=True)
@click.option('-sport', default=6001, help='server port of server', prompt=True)
@click.option('-lbport', default=5001, help='client port of load balancer', prompt=True)
@click.option('-lbIp', default="127.0.0.1", help='client port of load balancer', prompt=True)
def addsrv(cip, cport, sip, sport, lbip, lbport):
    if cip is None or cport is None or sip is None or sport is None or lbip is None or lbport is None:
        click.echo("Please specify valid ips and ports", err=True)
    else:
        click.echo("Adding Server @ %s:%s" % (sip, sport))
        p = multiprocessing.Process(target=add_new_server,
                                    args=(cip, cport, sip, sport, lbip, lbport),
                                    name='server')
        p.start()


@cli.command()
@click.option('-cip', default="127.0.0.1", help='ip of server', prompt=True)
@click.option('-cport', default=5002, help='port of server', prompt=True)
@click.option('-sip', default="127.0.0.1", help='ip of server', prompt=True)
@click.option('-sport', default=5001, help='port of server', prompt=True)
def addlb(cip, cport, sip, sport):
    if cip is None or cport is None or sip is None or sport is None:
        click.echo("Please specify valid ip and port.", err=True)
    else:
        click.echo("Adding Load Balancer at [%s:%s]" % (cip, cport))
        p = multiprocessing.Process(target=add_new_lb, args=(cip, cport, sip, sport),
                                    name='load-balancer')
        p.start()


def add_new_server(cip, cport, sip, sport, lbip, lbport):
    p = multiprocessing.current_process()
    click.echo("Starting Server with pid[%s], at [%s:%s]" % (p.pid, cip, cport))
    server = Server(cip, cport, sip, sport, lbip, lbport)
    server.start()


def add_new_lb(cip, cport, sip, sport):
    p = multiprocessing.current_process()
    click.echo("Starting Load Balancer with pid[%s], at [%s:%s]" % (p.pid, cip, cport))
    lb = LoadBalancer(cip, cport, sip, sport, )
    lb.start()


if __name__ == "__main__":
    cli()
