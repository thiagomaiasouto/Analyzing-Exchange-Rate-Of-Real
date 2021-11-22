"""This modules implements basic cli to perform executation of the ETL
and visualization pipeline
"""
from pathlib import Path
import click
from scripts.etl import ExchangeETL
from scripts.plots import GeneratePlots
from scripts.utils import parse_config, set_logger


@click.command()
@click.argument("config_file", type=str, default="./config.yml")
def etl(config_file: str) -> None:
    """
    ETL function that load raw data, apply transformations and export data
    Args:
        config_file (str): path to config file
    Returns:
        None
    """
    # parsing the configuration file YAML
    config = parse_config(config_file)

    # configuring the logger for this module
    logger = set_logger("run", config['log']['log_run_path'])

    # initializing files for verification
    processed_data = Path(config['etl']['processed_path'])
    plot1 = Path(config['plots']['plot1_path'])
    plot2 = Path(config['plots']['plot2_path'])

    # initalizing objects
    etl_pipeline = ExchangeETL(config_file)
    plot_pipeline = GeneratePlots(config_file)

    logger.info("Verifying if the processed dataframe file is already exists.")
    if processed_data.is_file() is False:
        logger.info(
            "The processed dataframe file doesn'exist, so the ETL will be performed.")
        etl_pipeline.processing()
        logger.info(
            "------ The ETL operations was terminated successfully -------")

        logger.info("Verifying if the plot1.png file is already exists.")
        if plot1.is_file() is False:
            logger.info("Generating the plot1")
            plot_pipeline.plot_graph1()
            logger.info("------- The plot1 was saved successfully --------")

        else:
            logger.info("------- The plot1 already exists --------")

        logger.info("Verifying if the plot2.png file is already exists.")
        if plot2.is_file() is False:
            logger.info("Generating the plot2")
            plot_pipeline.plot_graph2()
            logger.info("------- The plot2 was saved successfully --------")
        else:
            logger.info("------- The plot2 already exists --------")

    else:
        logger.info(
            "--------The processed dataframe file already exists.-------")

        logger.info("Verifying if the plot1.png file is already exists.")
        if plot1.is_file() is False:
            logger.info("Generating the plot1")
            plot_pipeline.plot_graph1()
            logger.info("------- The plot1 was saved successfully --------")
        else:
            logger.info("------- The plot1 already exists --------")

        logger.info("Verifying if the plot2.png file is already exists.")
        if plot2.is_file() is False:
            logger.info("Generating the plot2")
            plot_pipeline.plot_graph2()
            logger.info("------- The plot2 was saved successfully --------")
        else:
            logger.info("------- The plot2 already exists --------")


if __name__ == '__main__':
    etl()
