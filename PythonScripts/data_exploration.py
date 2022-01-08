def plots_dataExploration():
    import hvplot.pandas 
    import pandas as pd
    import numpy as np
    from sqlalchemy import create_engine
    import psycopg2
    from config import db_password

    ## Add the code to create the connection to the PostgrSQL db
    db_string = f"postgresql://postgres:{db_password}@127.0.0.1:5432/OlympicAnalysis_FP"
    #Create the database engine
    engine = create_engine(db_string) 
    #Tables named 'Olympics' and 'Indicators' will be returned as a dataframe.
    indicators_df = pd.read_sql_table('Indicators', engine)
    olympic_df = pd.read_sql_table('Olympics', engine)
    # list of previous years to olympics
    POYears = [1991, 1995, 1999, 2003, 2007, 2011, 2015, 2019]
    # only keep indicators corresponding to the years previous to the Olympics 
    ind_df = indicators_df[indicators_df.Year.isin(POYears)]
    # then label them with the actual year of the olympics, i.e.: 1991 in indicators is now 1992 (actual olympic year)
    ind_df.loc[:, 'Year'] = ind_df.loc[:, 'Year'] + 1

    # doing it using sql
    df_merge = pd.merge(ind_df, olympic_df, on = ["CountryCode", "Year"])
    columns_to_keep = ['Year','CountryCode','GDPCapita','GNICapita','Population','HDI','HDIRank','Top15']
    df_data = df_merge[columns_to_keep]
    # Plots of preliminary exploration
    plot_indsc = hvplot.scatter_matrix(df_data[['GDPCapita','GNICapita','Population','HDI','HDIRank','Top15']])
    hvplot.show(plot_indsc)

    plot_rangeinds = df_data.hvplot.scatter(x='Year', y=['GDPCapita', 'Population', 'HDI','Top15'], subplots=True, shared_axes=False, width=300, height=300).cols(2)
    hvplot.show(plot_rangeinds)

    plot_indscountry = df_data.hvplot.line(x='Year', y=['GDPCapita', 'Population', 'HDI','Top15'], subplots=True, shared_axes=False, width=200, height=300, groupby = 'CountryCode')
    hvplot.show(plot_indscountry)

    plot_olympicPerform = df_data.hvplot.bar(y='Top15', x = 'Year', groupby='CountryCode', height=400)
    hvplot.show(plot_olympicPerform)