import click
import requests

from prometheus_api_client import PrometheusConnect

@click.group()
def cli():
    pass

@cli.command()
def test():
    click.echo("Hello World")


@cli.command()
@click.option("--endpoint", default="http://localhost:9100")
def fetch_metrics(endpoint):
    p = PrometheusConnect(url=endpoint, disable_ssl=True)
    click.echo(p.all_metrics())


@cli.command()
@click.option("--endpoint", default="http://localhost:9100/metrics")
def scrape(endpoint):
    scraper(endpoint)

def scraper(endpoint):
    response = requests.get(endpoint)
    return(response.text)
        
def is_help(line):
    return line.startswith("# HELP")


def is_type(line):
    return line.startswith("# TYPE")

def get_value(line):
    return line.split(" ")[1]

def get_labels(line):
    labels = []
    if "{" not in line:
        return labels
    _labels = line.split(" ")[0]
    remaining = _labels.replace("}", "").split("{")[1]
    if "," in remaining:
        for thing in remaining.split(","):
            labels.append(thing.split("=")[0])
    else:
        labels.append(remaining.split("=")[0])    
    return labels
    
    
if __name__ == "__main__":
    cli()