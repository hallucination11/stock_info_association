import pymysql

conn_fin = pymysql.connect(user='query_user', password='kUsLN!RUaxk9nMxBG', port=9030, host='172.36.10.106')
cursor = conn_fin.cursor()
query_us_company = f"""
select A.sec_code, A.name_cn, B.company_name_cn, B.introduction_cn
            from hq_us_fin.us_security_base A left join hq_us_fin.us_company_info B on A.company_code = B.company_code
            where liste_state = '213001' and sec_type_code = '20000' and introduction_cn is NOT null;
"""
cursor.execute(query_us_company)
result_us_company = cursor.fetchall()

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
print(result_hk_company)
