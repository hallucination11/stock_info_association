import pymysql
import pandas as pd
import numpy as np
import boto3

conn_fin = pymysql.connect(user='query_user', password='kUsLN!RUaxk9nMxBG', port=9030, host='172.36.10.106')
cursor = conn_fin.cursor()
query_us_company = f"""
select A.sec_code, A.name_cn, B.company_name_cn, B.introduction_cn
            from hq_us_fin.us_security_base A left join hq_us_fin.us_company_info B on A.company_code = B.company_code
            where liste_state = '213001' and sec_type_code = '20000' and introduction_cn is NOT null;
"""
cursor.execute(query_us_company)
result_us_company = cursor.fetchall()
us_df = pd.DataFrame(list(result_us_company), columns=['sec_code', 'name', 'company_name', 'introduction'])

query_hk_company = f"""
select A.sec_code, A.name_cn, B.company_name, B.introduction
                                            from (select *
                                                  from hq_hk_fin.hq_security_base
                                                  where sec_type_code = '10000'
                                                    and liste_state = '213001') A
                                                     left join (select * from hq_hk_fin.hk_company_info_cn) B
                                                               on A.company_code = B.company_code
                                                ;
"""
cursor.execute(query_hk_company)
result_hk_company = cursor.fetchall()
hk_df = pd.DataFrame(list(result_hk_company), columns=['sec_code', 'name', 'company_name', 'introduction'])
company_df = pd.concat([us_df, hk_df], axis=0)

s3 = boto3.client('s3')
file_name = 'company_intro.csv'
bucket_name = 'hs-onedata'
object_key = 'algo/stock_info_association/origin_dataset/' + file_name
try:
    s3.upload_file(file_name, Bucket=bucket_name, Key=object_key)
    print(f"CSV 文件已成功上传到 S3 桶 {bucket_name} 中，对象键为 {object_key}")
    os.remove(file_name)
except Exception as e:
    print(f"上传到 S3 时发生错误: {str(e)}")
