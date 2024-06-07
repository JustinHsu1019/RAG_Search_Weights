import pandas as pd
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows

file_path = 'data/【測試結果】_60題.xlsx'
xls = pd.ExcelFile(file_path)

wb = openpyxl.load_workbook(file_path)

sheet_names = [f'alpha {i/10}' for i in range(10, 0, -1)]
for sheet in sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet)
    
    E_col = df.iloc[:, 4]
    F_col = df.iloc[:, 5]

    E_yes = E_col.value_counts().get('yes', 0)
    E_no = E_col.value_counts().get('no', 0)
    F_yes = F_col.value_counts().get('yes', 0)
    F_no = F_col.value_counts().get('no', 0)

    if (E_yes + E_no) > 0:
        E_percentage = E_yes / (E_yes + E_no) * 100
    else:
        E_percentage = 0
        
    if (F_yes + F_no) > 0:
        F_percentage = F_yes / (F_yes + F_no) * 100
    else:
        F_percentage = 0

    if sheet in wb.sheetnames:
        ws = wb[sheet]
    else:
        ws = wb.create_sheet(title=sheet)
        for row in dataframe_to_rows(df, index=False, header=True):
            ws.append(row)
    
    if ws.merged_cells:
        ws.unmerge_cells(str(ws.merged_cells.ranges))

    ws.cell(row=2, column=10).value = E_percentage
    ws.cell(row=2, column=11).value = F_percentage

wb.save('data/【測試結果】_60題_含準確率.xlsx')
