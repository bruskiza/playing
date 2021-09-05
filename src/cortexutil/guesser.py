import click
import requests
import logging as log
import json

log.basicConfig(level=log.INFO)

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
    print(scraper(endpoint))
    

@cli.command()
@click.option("--endpoint", default="http://localhost:9100/metrics")
def guess_metrics(endpoint):
    results = scraper(endpoint)
    guessed = {}
    for line in results.split("\n"):
        if (is_help(line)):
            metric = {}
            metric['name'] = None
            metric['type'] = None
            metric['value'] = None
            metric['labels'] = None
            
            metric['name'] = get_metric(line)
        elif (is_type(line)):
            metric['type'] = get_type(line)
        else:
            if has_labels(line):
                metric['labels'] = get_labels(line)
            if is_not_blank(line):
                metric['value'] = get_value(line)
        
        if (None in metric.values()):
            guessed[metric['name']] = metric
            
    
    print(json.dumps(guessed, indent=4))
    
    print(len(guessed.keys()))
            

def scraper(endpoint):
    log.info(f"Getting this endpoint: {endpoint}")
    response = requests.get(endpoint)
    log.info(response.status_code)
    return(response.text)
        
def is_help(line):
    return line.startswith("# HELP")

def is_type(line):
    return line.startswith("# TYPE")

def is_not_blank(line):
    return " " in line

def get_type(line):
    return line.split(" ")[3]

def get_value(line):
    log.info(line)
    if " " in line:
        return line.split(" ")[1]
    return ""

def has_labels(line):
    return "{" in line

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

def get_metric(line):
    if " " in line:
        return line.split(" ")[2]
    
    
if __name__ == "__main__":
    cli()