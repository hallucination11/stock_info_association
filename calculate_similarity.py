import faiss
import pandas as pd
import numpy as np

VECTOR_DIM = 1536
index = faiss.IndexFlatL2(VECTOR_DIM)


def transe_emb_index(embedding):
    embedding = np.array(embedding)
    index.add(embedding)
    return index


if __name__ == '__main__':

    comp_df = pd.read_csv('/Users/schencj/Desktop/hst/dataset/stock_information_association/company_intro_embedding.csv')
    comp_df = comp_df.dropna(subset=['embedding'])
    # info_df = pd.read_csv('/Users/schencj/Desktop/hst/dataset/stock_information_association/tmp.csv')
    stock_code_list = list(comp_df['sec_code'].values)
    embedding = comp_df['embedding'].values
    stock2index = dict()
    embedding_arr = []

    for i in range(len(embedding)):
        string_vector = embedding[i]
        string_vector = string_vector.strip('[]')
        string_elements = string_vector.split(', ')

        # 将字符串元素转换为浮点数
        float_vector = [float(element) for element in string_elements]
        embedding_arr.append(float_vector)
        stock2index[i] = stock_code_list[i]

    index.add(np.array(embedding_arr))

    info_df = pd.read_csv('/Users/schencj/Desktop/hst/dataset/stock_information_association/wrong_match_embedding.csv')
    info_embedding = info_df['embedding'].values

    for i in range(len(info_embedding)):
        string_vector = info_embedding[i]
        string_vector = string_vector.strip('[]')
        string_elements = string_vector.split(', ')

        query_vector = np.array([float(element) for element in string_elements])

        D, I = index.search(query_vector.reshape(1, -1), 3)
        # print("查询向量与最相似的向量的距离：", D)
        # reconstructed_vector = index.reconstruct(1)
        # print("找到的向量：", reconstructed_vector)
        print(i)
        # print("最相似的向量的索引：", I)
        print("最相似的向量的索引对应的股票代码：", stock2index[I[0][0]], stock2index[I[0][1]], stock2index[I[0][2]])

    # D, I = index.search(np.array(embedding_arr[10]).reshape(1, -1), 10)
    # print(I)


