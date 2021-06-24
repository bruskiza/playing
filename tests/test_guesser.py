from cortexutil.guesser import *
from click.testing import CliRunner


def test_is_help():
    assert is_help("HELP node_textfile_scrape_error 1") == False
    assert is_help("# HELP node_textfile_scrape_error 1") == True


def test_is_type():
    assert is_type("TYPE node_textfile_scrape_error 1") == False
    assert is_type("# TYPE node_textfile_scrape_error 1") == True


def test_get_value():
    result = get_value('promhttp_metric_handler_requests_total{code="503"} 0')
    assert result == "0"


def test_get_labels():
    result = get_labels(
        'prometheus_wal_watcher_records_read_total{consumer="3bac64",type="samples"} 7796'
    )
    assert len(result) == 2
    result = get_labels(
        'prometheus_wal_watcher_record_decode_failures_total{consumer="3bac64"}'
    )
    assert len(result) == 1
    result = get_labels("prometheus_web_federation_warnings_total 0")
    assert len(result) == 0


def test_scrape(mocker):
    mocker.patch("requests.get")
    scraper("http://foo")
    requests.get.assert_called_once_with("http://foo")


def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli, [])
    assert result.exit_code == 0


def test_test():
    runner = CliRunner()
    result = runner.invoke(test, [])
    assert "Hello World" in result.output


def test_fetch_metrics(mocker):
    mocker.patch.object(PrometheusConnect, "all_metrics")
    runner = CliRunner()
    result = runner.invoke(fetch_metrics, [])
    assert result.exit_code == 0
