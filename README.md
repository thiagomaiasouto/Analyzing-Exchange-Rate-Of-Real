# Analyzing-Exchange-Rate-Of-Real
This repository contains a data analysis tool that perform ETL operations and produces Explanatory Data Visualizations comparing the exchange rate of american dolar and brazilian real over the years. For the purpose of visualization has been used a lot of techniques like Gestalt Principles, Storytelling and Pre-Attenive attributes to improve the quality of graphs.

## Setup

1. Git Clone the repo
   ```
   git clone https://github.com/thiagomaiasouto/Exploring-eBay-Car-Sales-Data.git
   ```

2. Go to project root folder
   ```
   cd Exploring-eBay-Car-Sales-Data
   ```

3. Setup conda env in terminal
   ```
   conda create --name YOUR_ENVIROMENT_NAME python=3.8 --file requeriments.txt

   conda activate YOUR_ENVIROMENT_NAME
   ```

4. Run the code in the terminal
   
   ```
   python ./scripts/etl.py
   ```

5. To execute pylint and analyze the code format

    ```
    pylint ./scripts
    ```

6. After usage
   
   ```
   conda deactivate
   conda remove --name YOUR_ENVIROMENT_NAME --all
   ```

### The repository tree
```
├── README.md
├── requeriments.txt
├── .pylintrc
├── config.yml
├── __init__.py
├── run.py
├── .gitignore
|
├── data
│   ├── ECB_FX_USD-base.csv          
│   ├── Foreign_Exchange_Rates.csv              
│   ├── processed_data.csv  
|          
├── log
│   ├── etl.log
|   ├── plots.log
|   ├── run.log
|               
├── notebooks
│   └── Exchange_Rate_of_Real.ipynb
|
├── test
|   ├── __init__.py
|   ├── test_etl.py
|   |
|   ├── data_tests
|       └── euro-daily-hist_1999_2020.csv
|
├── visualizations
│   ├── plot1.png
|   ├── plot_notebook.png
|   └── plot_script.png
|
└── scripts
    ├── etl.py           
    ├── plots.py                
    └── utils.py

```
## Authors
- [Arthur Cunha](https://github.com/arthurfpcl22)
- [Thiago Maia](https://github.com/thiagomaiasouto)

## Credits
The overall structure of the project was heavily influenced by this [article](https://towardsdatascience.com/from-jupyter-notebook-to-sc-582978d3c0c).