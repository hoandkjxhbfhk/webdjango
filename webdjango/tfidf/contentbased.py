import pandas as pd
from shop.models import Product
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# from sqlalchemy import create_engine
# import pandas as pd

# # Tạo đối tượng kết nối đến cơ sở dữ liệu MySQL
# engine = create_engine('mysql+pymysql://root:@localhost/allbachelorshop')

# # Sử dụng Pandas để đọc dữ liệu từ đối tượng kết nối
# ds = pd.read_sql_query("SELECT * from shop_product", engine)

#ds = Product.objects.all()


def getFrames(ds):
    tf = TfidfVectorizer(analyzer="word", ngram_range=(1, 5), min_df=0, stop_words="english")
    tfidf_matrix = tf.fit_transform(ds[["name","category",]])
    print(tfidf_matrix)
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
    results = {}
    print(cosine_similarities)
    for idx, row in ds.iterrows():
        similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
        similar_items = [(cosine_similarities[idx][i], ds[i]) for i in similar_indices]

        results[row["id"]] = similar_items[1:]
    return results


def item(id):
    return (ds.loc[ds["id"] == id]["id"]).tolist()[0]


def recommend(item_id, num, results):
    ids = []
    recs = results[item_id][:num]
    for rec in recs:
        value = (ds.loc[ds["id"] == rec[1]]["id"]).tolist()[0]
        ids.append(value)
    df = ds[ds["id"].isin(ids)]
    return df
