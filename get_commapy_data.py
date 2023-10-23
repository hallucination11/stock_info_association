import pymysql

conn_fin = pymysql.connect(user='query_user', password='kUsLN!RUaxk9nMxBG', port=9030, host='172.36.10.106')
cursor = conn_fin.cursor()
query_us_company = f"""
select A.sec_code, A.name_cn, A.name_en, B.company_name_cn, B.company_name_en, B.introduction_cn
            from hq_us_fin.us_security_base A left join hq_us_fin.us_company_info B on A.company_code = B.company_code
            where liste_state = '213001' and sec_type_code = '20000' and A.sec_code limit 1;
"""
cursor.execute(query_us_company)
result_us_company = cursor.fetchall()
print(result)
