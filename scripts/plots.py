"""
This module implements the class GeneratePlots
that is responsible to create the plots and export them.
"""
import pandas as pd
from typing import List
from pathlib import Path
import logging
from .utils import set_logger, parse_config


class GeneratePlots():

    config_path: str 
    data_path: str 
    dataframe : pd.DataFrame
    logger : logging
    config : dict

    def __init__(self, config_path: str = "./config.yml") -> None:
        """
        Constructor to the class GeneratePlots
        """
        # initializing the config_path attribute
        self.config_path = config_path
                
        # loading config file in the config attribute
        self.config = parse_config(self.config_path)

        # configuring logger attribute
        self.logger = set_logger("plots", self.config['log']['log_plot_path'])
        self.logger.info("Plots config: %s", self.config['plots'])

        # initializing the data path attribute
        self.data_path = self.config['etl']['processed_path']

        # loading the processed dataframe
        self.dataframe = pd.read_csv(self.data_path)
    
    def plot_graph1(self) -> None:
        ...
     