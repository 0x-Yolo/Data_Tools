from WindPy import w
import datetime as dt
import pandas as pd
import data_organize as do

def main():
    table_name = input("输入你需要更新的表：")
    w.start()
    today=dt.datetime.today().strftime("%Y-%m-%d")
    data = do.get_data(table_name,how="raw")
    start_date,exist_date=do.data_time_tange(data)
    exist_date=pd.to_datetime(exist_date)
    #需要保证原始数据库的表头为wind代码
    index_code_list= ",".join(data.columns[1:].tolist())
    err,df= w.edb(index_code_list,exist_date,today,usedf=True)
    df.reset_index(inplace=True)
    df.rename(columns={'index':'date'},inplace=True)
    do.upload_data(df,table_name)
    print("您已经成功刷新数据")
    data=do.get_data(table_name)
    excel_name="test"+today+".xlsx"
    data.to_excel(excel_name)
    print("文件生成成功，请查看:"+excel_name)
    return data

if __name__ == "__main__":
    main()