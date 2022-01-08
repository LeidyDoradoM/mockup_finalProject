def cleaning_economics():
    import pandas as pd
    import numpy as np
    from sqlalchemy import create_engine
    import psycopg2
    from config import db_password

    #---- Reading World Bank Indicators 
    indicators_df = pd.read_csv('../Resources/WDIData.csv')
    # get rid off spaces in column names
    indicators_df.columns =[column.replace(" ", "") for column in indicators_df.columns]
    #----Cleaning the dataframe to keep only the information of interest--
    # list of development indicators to keep from the entire df
    indicators = ['GDP per capita, PPP (current international $)', 'GNI per capita, PPP (current international $)',
                'Population, total']
    # reading country codes file, saved from World Bank Website
    country_codes = pd.read_csv('../Resources/CountryCodes.csv')
    # Keep only rows with actual data
    country_codes = country_codes.dropna()
    # Keep only rows with country codes
    e_row = country_codes.index[country_codes['Country_Name'] == 'World'].tolist()
    country_codes = country_codes.drop(e_row)
    # convert the country codes as a list 
    countries  = country_codes.ISO3.tolist()

    # filtering the dataframe to keep only information corresponding to all the countries and the chosen indicators
    indicators_df.query('IndicatorName == @indicators & CountryCode == @countries', inplace = True)

    # Now we need to filter out the years.  We are going to make an analysis from 1990-2019
    years_to_keep = [str(i) for i in range(1990,2020)]
    columns_to_keep = ['CountryName','CountryCode','IndicatorName'] + years_to_keep
    # final indicators from World Bank DataCatalog
    features_df = indicators_df[columns_to_keep]
    # Reshape the tables such that the indicators will be columns and the years will be rows
    # Convert Years columns (1990-2019) of features dataframe(WB Indicators) to Rows
    df = features_df.melt(id_vars = ["CountryName", "CountryCode", "IndicatorName"], var_name="Year", value_name="Value")
    # Convert Indicators Rows to Columns using Pivot Table
    df_pivot = df.pivot_table('Value',['CountryName','CountryCode','Year'],'IndicatorName')
    # Convert Multindex pivot table to a dataframe again 
    features_df = pd.DataFrame(df_pivot.to_records())
    # convert type of column Year to integer
    features_df['Year'] = features_df['Year'].astype(int)
    # loading csv file of development indicators as dataframe
    hdi_df = pd.read_csv('../Resources/HumanDevelopmentIndex (HDI).csv', sep=',')
    # get rid off spaces in column names 
    hdi_df.columns =[column.replace(" ", "") for column in hdi_df.columns]
    hdi_df = hdi_df.dropna(how='all', axis=1)
    hdi_df["Country"] = hdi_df["Country"].str.strip()
    last_i = hdi_df.index[hdi_df['Country'] == 'Zimbabwe'].tolist()
    hdi_df = hdi_df.iloc[0:last_i[0]+1]
    hdi_df = hdi_df.melt(id_vars=['Country','HDIRank'], var_name = "Year", value_name = "HDI")
    hdi_df.rename({'Country': 'CountryName'}, axis = 'columns', inplace = True )
    hdi_df['HDIRank'] = hdi_df['HDIRank'].astype(int)
    hdi_df['Year'] = hdi_df['Year'].astype(int)
    hdi_df['HDI'] = hdi_df['HDI'].replace('..',np.nan)
    hdi_df['HDI'] = hdi_df['HDI'].astype(float)

    df_merge = pd.merge(features_df, hdi_df, on = ["CountryName", "Year"])
    # Reorganize order of columns and rename some of them
    cols = ['Year','CountryCode','CountryName', 'GDP per capita, PPP (current international $)','GNI per capita, PPP (current international $)',
            'Population, total', 'HDIRank','HDI']
    df_merge = df_merge[cols]
    df_merge.rename(columns = {'GDP per capita, PPP (current international $)':'GDPCapita', 
                            'GNI per capita, PPP (current international $)':'GNICapita',
                            'Population, total':'Population'}, inplace=True)

    ## Add the code to create the connection to the PostgrSQL db
    db_string = f"postgresql://postgres:{db_password}@127.0.0.1:5432/OlympicAnalysis_FP"
    #Create the database engine
    engine = create_engine(db_string)     
    ## Add df_merge to a SQL db
    df_merge.to_sql(name = 'Indicators', con = engine, if_exists = 'replace', index = False) 

