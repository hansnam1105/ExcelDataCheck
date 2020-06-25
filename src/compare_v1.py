def compare_excel(old_xlsx, new_xlsx, column_name):
    import pandas as pd

    df_old = pd.read_excel(old_xlsx)
    df_new = pd.read_excel(new_xlsx)

    # 불러온 데이터의 버전 구분
    df_old['ver'] = 'old'
    df_new['ver'] = 'new'

    id_dropped = set(df_old[column_name]) - set(df_new[column_name])
    id_added = set(df_new[column_name]) - set(df_old[column_name])

    # 삭제된 데이터
    df_dropped = df_old[df_old[column_name].isin(id_dropped)].iloc[:, :-1]
    # 추가된 데이터
    df_added = df_new[df_new[column_name].isin(id_added)].iloc[:, :-1]

    df_concatted = pd.concat([df_old, df_new], ignore_index=True)
    changes = df_concatted.drop_duplicates(df_concatted.columns[:-1], keep='last')
    duplicated_list = changes[changes[column_name].duplicated()][column_name].to_list()
    df_changed = changes[changes[column_name].isin(duplicated_list)]

    df_changed_old = df_changed[df_changed['ver'] == 'old'].iloc[:, :-1]
    df_changed_old.sort_values(by=column_name, inplace=True)

    df_changed_new = df_changed[df_changed['ver'] == 'new'].iloc[:, :-1]
    df_changed_new.sort_values(by=column_name, inplace=True)

    # 정보가 변경된 데이터 정리
    df_info_changed = df_changed_old.copy()
    for i in range(len(df_changed_new.index)):
        for j in range(len(df_changed_new.columns)):
            if (df_changed_new.iloc[i, j] != df_changed_old.iloc[i, j]):
                df_info_changed.iloc[i, j] = str(df_changed_old.iloc[i, j]) + " ==> " + str(df_changed_new.iloc[i, j])

    # 엑셀 저장            
    with pd.ExcelWriter('C:/Users/hansn/PycharmProjects/ExcelDataCheck/example/compared_result.xlsx') as writer:
        df_info_changed.to_excel(writer, sheet_name='info changed', index=False)
        df_added.to_excel(writer, sheet_name='added', index=False)
        df_dropped.to_excel(writer, sheet_name='dropped', index=False)

from tkinter import Tk
from tkinter.filedialog import askopenfilename

Tk().withdraw()
filename = askopenfilename()
print(filename)
filename2 = askopenfilename()
print(filename2)
column_val = input("컬럼 명을 입력해주세요: ")
print(column_val)
compare_excel(filename, filename2, column_val)