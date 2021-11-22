"""
This module implements the class GeneratePlots
that is responsible to create the plots and export them.
"""
import logging
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
from .utils import set_logger, parse_config


class GeneratePlots():
    """
    This class is responsible to perform preprocessing steps
    in the dataset and for plot and export the graphs
    """

    config_path: str
    data_path: str
    dataframe: pd.DataFrame
    logger: logging
    config: dict
    fhc: pd.DataFrame
    lula: pd.DataFrame
    dilma: pd.DataFrame
    temer: pd.DataFrame
    bolsonaro: pd.DataFrame
    selected: pd.DataFrame
    covid: pd.DataFrame

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
        self.logger.info("The processed dataframe was loaded succesfully.")

        # converting the column 'Date' to datetime type
        self.dataframe['Date'] = pd.to_datetime(self.dataframe['Date'])
        self.logger.info(
            "The type of the column 'Date' was changed to datetime type.")

    def plot_graph1_preprocessing(self) -> None:
        """
         This function is responsible to preprocess the Dataframe
         for using it in the plot of BRL Exchange rate for president
        """

        # obtaining the period of FHC government
        filter1 = self.dataframe['Date'].dt.year >= 2000
        filter2 = self.dataframe['Date'].dt.year < 2003
        self.fhc = self.dataframe.copy()[filter1 & filter2]
        self.logger.info("The period of FHC government was selected.")

        # obtaining the period of LULA government
        filter3 = self.dataframe['Date'].dt.year >= 2003
        filter4 = self.dataframe['Date'].dt.year < 2011
        self.lula = self.dataframe.copy()[filter3 & filter4]
        self.logger.info("The period of LULA government was selected.")

        # obtaining the period of DILMA government
        filter5 = self.dataframe['Date'].dt.year >= 2010
        filter6 = self.dataframe['Date'].dt.year < 2017
        self.dilma = self.dataframe.copy()[filter5 & filter6]
        self.logger.info("The period of DILMA government was selected.")

        # obtaining the period of TEMER government
        filter7 = self.dataframe['Date'].dt.year >= 2017
        filter8 = self.dataframe['Date'].dt.year < 2018
        self.temer = self.dataframe.copy()[filter7 & filter8]
        self.logger.info("The period of TEMER government was selected.")

        # obtaining the period of BOLSONARO government
        filter9 = self.dataframe['Date'].dt.year >= 2018
        self.bolsonaro = self.dataframe.copy()[filter9]
        self.logger.info("The period of BOLSONARO government was selected.")

        # applying the rolling mean to the FHC dataframe
        self.fhc['BRL'] = self.fhc['BRL'].rolling(2).mean()
        self.logger.info("The rolling mean was applied to FHC dataframe.")

        # applying the rolling mean to the LULA dataframe
        self.lula['BRL'] = self.lula['BRL'].rolling(2).mean()
        self.logger.info("The rolling mean was applied to LULA dataframe.")

        # applying the rolling mean to the DILMA dataframe
        self.dilma['BRL'] = self.dilma['BRL'].rolling(2).mean()
        self.logger.info("The rolling mean was applied to DILMA dataframe.")

        # applying the rolling mean to the TEMER dataframe
        self.temer['BRL'] = self.temer['BRL'].rolling(2).mean()
        self.logger.info("The rolling mean was applied to TEMER dataframe.")

        # applying the rolling mean to the BOLSONARO dataframe
        self.bolsonaro['BRL'] = self.bolsonaro['BRL'].rolling(2).mean()
        self.logger.info(
            "The rolling mean was applied to BOLSONARO dataframe.")

    def plot_graph1(self) -> None:
        """
         This function is responsible to apply the preprocessing steps in
         the Dataframe and for create and export the plot of BRL Exchange rate for president
        """

        # preprocessing data
        self.plot_graph1_preprocessing()

        # adding the FiveThirtyEight style
        style.use('fivethirtyeight')
        self.logger.info("The plot style was changed to 'fivethirtyeight'.")

        # adding the subplots
        plt.figure(figsize=(12, 6))
        ax1 = plt.subplot(2, 5, 1)
        ax2 = plt.subplot(2, 5, 2)
        ax3 = plt.subplot(2, 5, 3)
        ax4 = plt.subplot(2, 5, 4)
        ax5 = plt.subplot(2, 5, 5)
        ax6 = plt.subplot(2, 1, 2)
        self.logger.info("The subplots were created.")

        axes = [ax1, ax2, ax3, ax4, ax5, ax6]

        # applying changed to all subplots
        for axe in axes:
            axe.set_ylim(0.5, 2.0)
            axe.set_yticks([1.0, 2.0, 3.5, 5.0, 6.0])
            axe.set_yticklabels(['1.0', '2.0', '3.5', '5.0', '6.0'],
                                alpha=0.3)
            axe.set_xticklabels([])
            axe.grid(alpha=0.5)

        self.logger.info("The changes were applied to all subplots.")

        # ax1: FHC
        ax1.plot(self.fhc['Date'], self.fhc['BRL'],
                 color='#BF5FFF')
        ax1.set_xticklabels(
            ['', '2000', '', '', '', '2001', '', '', '', '2002'], alpha=0.3)
        ax1.text(730380.0, 6.3, '(2000-2002)', weight='bold',
                 alpha=0.3)
        self.logger.info("The FHC plot was created.")

        # ax2: LULA
        ax2.plot(self.lula['Date'], self.lula['BRL'],
                 color='#ffa500')
        ax2.set_xticklabels(['', '2002', '', '2004', '', '2006', '',
                            '2008', '', '2010'], alpha=0.3)
        ax2.text(732288.0, 6.92, 'LULA', fontsize=18, weight='bold',
                 color='#ffa500')
        ax2.text(732038.0, 6.3, '(2003-2008)', weight='bold',
                 alpha=0.3)
        self.logger.info("The LULA plot was created.")

        # ax3: DILMA
        ax3.plot(self.dilma['Date'], self.dilma['BRL'],
                 color='#646464')
        ax3.set_xticklabels(['', '2010', '', '', '2013', '',
                             '', '', '2016'], alpha=0.3)
        ax3.text(734705.0, 6.92, 'DILMA', fontsize=18, weight='bold',
                 color='#646464')
        ax3.text(734485.0, 6.3, '(2011-2016)', weight='bold',
                 alpha=0.3)
        self.logger.info("The DILMA plot was created.")

        # ax4: TEMER
        ax4.plot(self.temer['Date'], self.temer['BRL'],
                 color='#86BE3C')
        ax4.set_xticklabels(['', '2017', '', '',
                             '', '2018', ''], alpha=0.3)
        ax4.text(736445.0, 6.92, 'TEMER', fontsize=18, weight='bold',
                 color='#86BE3C')
        ax4.text(736420.0, 6.3, '(2017-2018)', weight='bold',
                 alpha=0.3)
        self.logger.info("The TEMER plot was created.")

        # ax5: BOLSONARO
        ax5.plot(self.bolsonaro['Date'], self.bolsonaro['BRL'],
                 color='#C33734')
        ax5.set_xticklabels(['', '2019', '', '', '2020', '', '', '2021', ''],
                            alpha=0.3)
        ax5.text(737000.0, 6.92, 'BOLSONARO', fontsize=18, weight='bold',
                 color='#00B2EE')
        ax5.text(737100.0, 6.3, '(2019-2021)', weight='bold',
                 alpha=0.3)
        self.logger.info("The BOLSONARO plot was created.")

        # ax6: TODOS OS PRESIDENTES
        ax6.plot(self.fhc['Date'], self.fhc['BRL'],
                 color='#BF5FFF')
        ax6.plot(self.lula['Date'], self.lula['BRL'],
                 color='#ffa500')
        ax6.plot(self.dilma['Date'], self.dilma['BRL'],
                 color='#646464')
        ax6.plot(self.temer['Date'], self.temer['BRL'],
                 color='#86BE3C')
        ax6.plot(self.bolsonaro['Date'], self.bolsonaro['BRL'],
                 color='#C33734')
        ax6.grid(alpha=0.5)
        ax6.set_xticks([])
        self.logger.info("The plot with all presidents was created.")

        # addind the title and subtitle
        ax1.text(730016.0, 9.35, "COTAÇÃO USD-REAL ENTRE 2000-2021",
                 fontsize=20, weight='bold')
        ax1.text(
            730016.0,
            8.14,
            """EURO-USD taxas de câmbio para o governo FHC (2000 - 2002), LULA (2002-2010),
                Dilma (2010-2016), Temer(2017-2018), Bolsonaro(2018-2021)""",
            fontsize=16)
        self.logger.info("The title and subtitle were added to the plot.")

        # adding a signature
        ax6.text(
            729916.0,
            0.65,
            "DCA0305" +
            " " *
            190 +
            "Arthur França/Thiago Maia",
            color='#f0f0f0',
            backgroundcolor='#4d4d4d',
            size=14)
        self.logger.info("The signature was added to the plot.")

        # exporting the first graph
        plt.savefig(self.config['plots']['plot1_path'])
        self.logger.info("The first graph was saved successfully.")

    def plot_graph2_preprocessing(self) -> None:
        """
         This function is responsible to preprocess the Dataframe
         for using it in the plot of BRL Exchange rate in covid 19 period
        """

        # obtaining the period of the plot
        filter1 = self.dataframe['Date'].dt.year >= 2016
        filter2 = self.dataframe['Date'].dt.year < 2021
        self.selected = self.dataframe.copy()[filter1 & filter2]
        self.logger.info("The period of plot was selected.")

        # obtaining the period of the covid-19
        filter3 = self.dataframe['Date'].dt.year >= 2019
        self.covid = self.dataframe.copy()[filter3 & filter2]
        self.logger.info("The period of covid-19 was selected.")

    def plot_graph2(self) -> None:
        """
         This function is responsible to apply the preprocessing steps in
         the Dataframe and for create and export the plot of BRL Exchange rate for covid-19
        """

        # preprocessing data
        self.plot_graph2_preprocessing()

        # adding the FiveThirtyEight style
        style.use('fivethirtyeight')
        self.logger.info("The plot style was changed to 'fivethirtyeight'.")

        # adding the selected period to plot
        _, axe = plt.subplots(figsize=(12, 6))
        axe.plot(self.selected['Date'], self.selected['BRL'],
                 linewidth=1, color='#A6D785')
        self.logger.info("The selected period was plotted.")

        # adding the covid-19 period to plot
        axe.plot(self.covid['Date'], self.covid['BRL'],
                 linewidth=3, color='#e23d28')
        self.logger.info("The covid-19 period was plotted.")

        # highlihting the peak of the crisis
        axe.axvspan(xmin=737412.0, xmax=737602.0, ymin=0.03,
                    alpha=0.3, color='grey')
        self.logger.info("The highlihting to the peak crisis was added.")

        # adding separete tick labels
        axe.set_xticklabels([])
        axe.set_yticklabels([])
        self.logger.info("The separate tick labels was added.")

        x_coord = 735945.0
        for year in ['2016', '2017', '2018', '2019', '2020', '2021']:
            axe.text(x_coord, 2.75, year, alpha=0.5, fontsize=16)
            x_coord += 365
        self.logger.info("The x ticks was added.")

        y_coord = 3.05
        for rate in ['3.0', '4.0', '5.0', '6.0']:
            axe.text(735800.0, y_coord, rate, alpha=0.5, fontsize=16)
            y_coord += 1.0
        self.logger.info("The y ticks was added.")

        # adding a title and a subtitle
        axe.text(
            735800.0,
            6.67,
            "Real-USD rate peaked at 5.88 during 2020's Covid crises",
            weight='bold',
            fontsize=18)
        axe.text(735800, 6.40, 'Real-USD exchange rates between 2016 and 2021',
                 size=16)
        self.logger.info("The title and subtitle were added.")

        # exporting the second graph
        plt.savefig(self.config['plots']['plot2_path'])
        self.logger.info("The second graph was saved successfully.")
