import cleaningIndicators as cI
import cleaningOlympics as cO
import data_exploration as de

print('This is a test of cleaning data and loading into pdAdmin')
print('Exporting the economic indicators to the db ...')
cI.cleaning_economics()
print('all done')
print("Exporting the olympic games table to the db ...")
cO.cleaning_olympics()

print('Now data exploration...')
de.plots_dataExploration()

print('All Done!')


