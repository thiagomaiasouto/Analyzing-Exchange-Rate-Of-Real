"""This modules implements basic cli to perform executation of the ETL
and visualization pipeline
"""

from scripts.etl import ExchangeETL
import click



@click.command()
@click.argument("config_file", type=str, default="./config.yml")
def etl(config_file: str) -> None:
    """
    ETL function that load raw data, apply transformations and export data
    Args:
        config_file [str]: path to config file
    Returns:
        None
    """
    #ETL = ExchangeETL(config_file)
    click.echo(f"O arquivo {config_file} foi carregado com sucesso.")
    #ETL.processing()

    


if __name__ == '__main__':
    etl()
