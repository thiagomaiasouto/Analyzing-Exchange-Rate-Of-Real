"""This modules implements basic cli to perform executation of the ETL
and visualization pipeline
"""

from scripts.etl import ExchangeETL
from scripts.plots import GeneratePlots
from pathlib import Path
import click

from scripts.utils import parse_config, set_logger



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
    config = parse_config(config_file)
    
    logger = set_logger("run", config['log']['log_run_path'])

    processed_data = Path(config['etl']['processed_path'])

    logger.info("Verifying if the processed dataframe file is already exists.")
    if processed_data.is_file() is False:
        logger.info("The processed dataframe file doesn'exist, so the ETL will be performed.")
        ETL = ExchangeETL(config_file)
        ETL.processing()
        logger.info("------ The ETL operations was terminated successfully -------")

    else:
        logger.info("The processed dataframe file already exists.")
        #logger.info("Verifying if the plots images file already exists.")
        PLOT = GeneratePlots(config_file)
        logger.info("Generating the plot1")
        PLOT.plot_graph1()
        logger.info("------- The plot1 was saved successfully --------")
        

    

    


if __name__ == '__main__':
    etl()
