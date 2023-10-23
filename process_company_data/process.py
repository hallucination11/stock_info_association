import pandas as pd
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm

pd.set_option('display.max_columns', None)  # 显示所有列
pd.set_option('display.max_rows', None)  # 显示所有行
pd.set_option('display.width', None)  # 自动调整列宽
pd.set_option('display.max_colwidth', None)  # 显示所有单元格的内容


def get_embedding(text):
    url = "https://one-api.hszq8.com/v1/embeddings"
    headers = {
        "Authorization": "Bearer sk-XMDta0ZD8hUuTnTC39B7Cf43AfE743C2877e2e875f5f1aD7",
        "Content-Type": "application/json"
    }
    data = {
        "input": text,
        "model": "text-embedding-ada-002",
        "encoding_format": "float"
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        # 请求成功
        result = response.json()
        return result['data'][0].get('embedding')


if __name__ == '__main__':
    comp_df = pd.read_csv("/Users/schencj/Desktop/hst/dataset/stock_information_association/company_intro.csv")
    comp_df['introduction'] = comp_df['introduction'].apply(lambda x: BeautifulSoup(x, "html.parser").text)
    for i in tqdm(range(len(comp_df))):
        if comp_df['type'].iloc[i] == 'hk':
            prompt = f"""
            在港股市场中，{comp_df['company_name'].iloc[i]}的股票名称为{comp_df['name'].iloc[i]}, 股票代码为{comp_df['sec_code'].iloc[i]}, 简介为{comp_df['introduction'].iloc[i]}
            """
        else:
            prompt = f"""
            在美股市场中，{comp_df['company_name'].iloc[i]}的股票名称为{comp_df['name'].iloc[i]}, 股票代码为{comp_df['sec_code'].iloc[i]}, 简介为{comp_df['introduction'].iloc[i]}
            """
        embedding = get_embedding(prompt)

    df = pd.read_csv('/Users/schencj/Desktop/hst/dataset/stock_information_association/tmp.csv')
    print(df['txt_extract'])
    print(df['embedding'])
