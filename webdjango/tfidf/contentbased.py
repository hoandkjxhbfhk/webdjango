# import numpy as np
# import pandas as pd
# import pymysql
# import time
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import linear_kernel

# connection = pymysql.connect(host="localhost", user="root",password= "", database="allbachelorshop")
# ds = pd.read_sql_query("SELECT * from shop_product", connection)


# def getFrames(ds):
#     tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 5),
#                          min_df=0, stop_words='english')
#     tfidf_matrix = tf.fit_transform(ds['name'])

#     cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
#     results = {}

#     for idx, row in ds.iterrows():
#         similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
#         similar_items = [(cosine_similarities[idx][i], ds['id'][i])
#                          for i in similar_indices]

#         results[row['id']] = similar_items[1:]
#     return results


# def item(id):
#     return (ds.loc[ds['id'] == id]['id']).tolist()[0]


# def recommend(item_id, num, results):
#     ids = []
#     recs = results[item_id][:num]
#     for rec in recs:
#         value = (ds.loc[ds['id'] == rec[1]]['id']).tolist()[0]
#         ids.append(value)
#     df = ds[ds['id'].isin(ids)]
#     return df


# connection.close()
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from shop.models import Product

def getFrames():
    # ds = Product.objects.all()

    # tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 5),
    #                      min_df=0, stop_words='english')
    # tfidf_matrix = tf.fit_transform([product.name for product in ds])

    # cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
    results = {}

    # for idx, product in enumerate(ds):
    #     similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
    #     similar_items = [(cosine_similarities[idx][i], ds[i].id)
    #                      for i in similar_indices]

    #     results[product.id] = similar_items[1:]
    return results

def recommend(item_id, num, results):
    ids = []
    recs = results[item_id][:num]
    for rec in recs:
        ids.append(rec[1])
    return Product.objects.filter(id__in=ids)

results = getFrames()
