from .models import Wine,Review,Cluster
from django.contrib.auth.models import User
from sklearn.cluster import KMeans
from scipy.sparse import dok_matrix, csr_matrix
import numpy as np
def update_clusters():
    num_reviews = Review.objects.count()
    print (num_reviews)
    # update_step = ((num_reviews/100)+1) * 5
    update_step = 6
    print (update_step)
    if num_reviews % update_step == 0: # using some magic numbers here, sorry...
        # Create a sparse matrix from user reviews
        all_user_names = list(map(lambda x: x.username, User.objects.only("username")))
        all_wine_ids = set(map(lambda x: x.wine.id, Review.objects.only("wine")))
        num_users = len(all_user_names)
        ratings_m = dok_matrix((num_users, max(all_wine_ids)+1), dtype=np.float32)
        for i in range(num_users): # each user corresponds to a row, in the order of all_user_names
            user_reviews = Review.objects.filter(user_name=all_user_names[i])
            for user_review in user_reviews:
                ratings_m[i,user_review.wine.id] = user_review.rating

        # Perform kmeans clustering
        k = int(num_users / 10) + 2
        kmeans = KMeans(n_clusters=k)
        clustering = kmeans.fit(ratings_m.tocsr())

        # Update clusters
        Cluster.objects.all().delete()
        new_clusters = {i: Cluster(name=i) for i in range(k)}
        for cluster in new_clusters.values(): # clusters need to be saved before referring to users
            cluster.save()
        for i,cluster_label in enumerate(clustering.labels_):
            new_clusters[cluster_label].users.add(User.objects.get(username=all_user_names[i]))

        print (new_clusters)




"""
from .models import Wine, Review, Cluster
from django.contrib.auth.models import User
from sklearn.cluster import KMeans
from scipy.sparse import csr_matrix
import numpy as np

def update_clusters():
    num_reviews = Review.objects.count()
    update_step = 100  # Thay đổi mỗi khi có 100 đánh giá mới

    if num_reviews % update_step == 0:
        # Lấy danh sách tên người dùng và ID của tất cả các loại rượu
        all_user_names = User.objects.values_list('username', flat=True)
        all_wine_ids = Wine.objects.values_list('id', flat=True)

        num_users = len(all_user_names)
        num_wines = len(all_wine_ids)

        # Tạo ma trận đánh giá của người dùng và loại rượu
        ratings_m = csr_matrix((num_users, num_wines), dtype=np.float32)
        user_dict = {user_name: i for i, user_name in enumerate(all_user_names)}
        wine_dict = {wine_id: j for j, wine_id in enumerate(all_wine_ids)}

        # Cập nhật ma trận đánh giá
        for review in Review.objects.all():
            user_idx = user_dict.get(review.user_name)
            wine_idx = wine_dict.get(review.wine_id)
            if user_idx is not None and wine_idx is not None:
                ratings_m[user_idx, wine_idx] = review.rating

        # Tính toán số lượng cụm thích hợp
        k = min(int(num_users / 10) + 2, num_users)
        
        # Thực hiện phân cụm bằng thuật toán KMeans
        kmeans = KMeans(n_clusters=k)
        clustering = kmeans.fit(ratings_m)

        # Cập nhật các cụm
        Cluster.objects.all().delete()
        new_clusters = {i: Cluster(name=i) for i in range(k)}
        for cluster in new_clusters.values():
            cluster.save()
        for user_idx, cluster_label in enumerate(clustering.labels_):
            user_name = all_user_names[user_idx]
            new_clusters[cluster_label].users.add(User.objects.get(username=user_name))

        print(new_clusters)
"""