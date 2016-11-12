import click


@click.group()
def cli():
    click.echo("Distributed Key Value Store.")


@cli.command()
@click.option('-ip', help='ip of the server', prompt=True)
@click.option('-port', help='port of the server', prompt=True)
def addsrv(ip, port):
    if ip is None or port is None:
        click.echo("Please specify valid ip and port.")
    else:
        click.echo("Adding server @ %s:%s" % (ip, port))


@cli.command()
@click.option('-ip', help='ip of load balancer', prompt=True)
@click.option('-port', help='port of load balancer', prompt=True)
def addlb(ip, port):
    if ip is None or port is None:
        click.echo("Please specify valid ip and port.")
    else:
        click.echo("Adding load balancer @ %s:%s" % (ip, port))

