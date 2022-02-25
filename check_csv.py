#%%
import csv


#%% 
with open('laposte_hexasmal.csv') as f_input:
    csv_input = csv.reader(f_input)
    header = next(csv_input)
    expected = len(header)
    
    for line_number, row in enumerate(csv_input, start=2):
        l_champs = row[0].split(';')
        

        if len(l_champs) > 5:
            try:
                float(l_champs[5])
                float(l_champs[6])
            except:
                print(f'Problème ligne {line_number} : {row[0]}')

# %%
