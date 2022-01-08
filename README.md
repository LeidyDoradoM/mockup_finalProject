# Predicting Number of Medals Won in the Summer Olympic Games by Participated Countries

In our final project, we are interested in analyze how different economic, social and/or political factors could impact the performance of countries when they participate in the Summer Olympic Games. The performance is quantify as the total number of medals won by each country in each Olympic Game.

## 1. Data Exploration:

Economic and Political Indicators will be draw from the [**World Bank Data Catalog**](https://datacatalog.worldbank.org/search/dataset/0037712/World-Development-Indicators) that has around 1453 indicators compiled from official sources around the world (204 countries are considered). The original data has initially been explored by using `Python-Pandas Library`. The jupyter notebook is found [here](https://github.com/JoeAB3/Group5Capstone_Project/blob/Leidybranch/pre-processingWBD.ipynb).  
In addition to this dataset, we have added another index from [**United Nations**](http://hdr.undp.org/en/indicators/137506#). This is the *Human Development Index(HDI)*, which "measures average achievement in three basic dimensions of human development: long and healthy life, knowledge and decent standard of living. 

With these two datasets we have created a joined dataframe that contains four indicators measured anually and for each country.  Because the HDI has been only reported since 1990, we are considered only the frame of time: 1990-2019.  

## 2. Machine Learning:

Our goal is to predict the total number of medals won by each country in the Summer Olympic Games. Because, the olympic games are dominated for 3 or 4 countries, this data will be highly skewed.  Therefore, we need to use a Regression Model that can handle this kind of data. We would need to analyze further the data and to do some research that allows us to find the more suitable model.

## 3. Database:

Due to the nature of our data, we will use a PostgreSQL database to save our data sets. Our database will initially have two tables: `Indicators` and `OlympicMedals`. Below there is a rough schema of each table:

```sql
CREATE TABLE Indicators (
  Country_Code character(3) NOT NULL,
  GDP_growth integer NOT NULL,
  GNI_growth integer NOT NULL,
  Population integer NOT NULL,
  Year character NOT NULL,
  HDI integer NOT NULL,
  HDI_Rank integer NOT NULL
);

CREATE TABLE Olympics(
  Country_Code character(3) NOT NULL,
  Year integer NOT NULL,
  GOLD_Medals integer NOT NULL,
  SILVER_Medals integer NOT NULL,
  BRONZE_Medals integer NOT NULL,
  TOTAL_Medals integer NOT NULL
);
```
After we clean and pre-process the original datasets in Jupyter Notebook, we will write them to `PostgreSQL` tables.
While in `PgAdmin` we will need to create the database and tables with the schema presented above.