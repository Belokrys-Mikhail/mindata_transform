import pandas as pd

filepath = r'C:\Users\Algis\Desktop\Belokrys\Программы\Min_modifier\samples\ok exp 2405.txt'
raw_data = pd.read_csv(filepath, header=None)

for i in range(len(raw_data)):
    raw_data.iloc[i] = raw_data.iloc[i].str.split()


    
        
rows_to_del = []
for i in range(len(raw_data)):
    if raw_data.iloc[i][0][0][:3] in ('---', 'Ele', 'Tot'):
        rows_to_del.append(i)       
data = raw_data.drop(rows_to_del)




for i in range(len(data)):
    if len(data.iloc[i][0]) >= 4:
        data.iloc[i][0] = data.iloc[i][0][:1] + data.iloc[i][0][2:]



    
data = data.reset_index()
data = pd.DataFrame(data[0].to_list(), columns = ['Elem', 'Wt, %', 'At, %'])
data = data.drop(columns=['At, %'])




sample_index_list = []
sample_name_list = []
point_index_list = []
point_name_list = []
    
for i in range(len(data)):
    if data['Elem'].iloc[i] == 'sample':
        sample_index_list.append(i)
        sample_name_list.append(data['Elem'].iloc[i] + ' ' + data['Wt, %'].iloc[i])
    elif data['Elem'].iloc[i] == 'sp':
        point_index_list.append(i)
        point_name_list.append(data['Elem'].iloc[i] + ' ' + str(data['Wt, %'].iloc[i]))
        



for i in range(len(data)):
    try:
        data['Wt, %'].iloc[i] = float(data['Wt, %'].iloc[i])
    except:
        continue
    



sample_index_list.append(len(data) + 1)
point_index_list.append(len(data) + 1)
    
sample_indexes = list(zip(sample_index_list, sample_index_list[1:]))
point_indexes = list(zip(point_index_list, point_index_list[1:]))

sample_indexes_dict = {}
point_indexes_dict = {}

for i in range(len(sample_name_list)):
    sample_indexes_dict[sample_indexes[i]] = sample_name_list[i]
    
for i in range(len(point_name_list)):
    point_indexes_dict[point_indexes[i]] = point_name_list[i]
    



sample_index_pre_df = []
point_index_pre_df = []

for key, value in sample_indexes_dict.items():
    sample_index_pre_df.extend([value] * (key[1] - key[0]))

for key, value in point_indexes_dict.items():
    point_index_pre_df.extend([value] * (key[1] - key[0]))
    



sample_index_df = pd.DataFrame(sample_index_pre_df)
point_index_df = pd.DataFrame(point_index_pre_df)
    
data = data.assign(sample=sample_index_df)
    
point_index_df.loc[-1] = '0'
point_index_df.index = point_index_df.index + 1
point_index_df.sort_index(inplace=True)
    
data = data.assign(point=point_index_df)




rows_to_del = []

for i in range(len(data)):
    if data['Elem'].iloc[i] in ('sample', 'sp'):
        rows_to_del.append(i)
        
data = data.drop(rows_to_del)



reshaped_data = pd.pivot_table(data, values='Wt, %', index=['sample', 'point'], columns='Elem', aggfunc='sum', fill_value=0, margins=True, dropna=True, margins_name='Total')



from pandas import ExcelWriter
filepath = filepath[:-4:] + '_r.xlsx'

writer = ExcelWriter(filepath)
reshaped_data.to_excel(writer, 'Sheet1')
writer.save()

print('SUCCESSFULLY')