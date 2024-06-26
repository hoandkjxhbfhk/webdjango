import numpy as np
import pandas as pd
import scipy as sp
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from shop.models import Product, Review  # Thêm import cho mô hình Product và Review
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.neighbors import NearestNeighbors


@login_required
def recommendation(request):
    products = Product.objects.all()  # Sử dụng queryset của Django để lấy tất cả sản phẩm
    ratings = Review.objects.all()  # Sử dụng queryset để lấy tất cả đánh giá

    # Tính toán điểm đánh giá trung bình và số lượng đánh giá cho từng sản phẩm
    avg_ratings = {}
    num_ratings = {}
    last_rating = {}

    for rating in ratings:
        product_id = rating.product_id
        if product_id not in avg_ratings:
            avg_ratings[product_id] = rating.rating
            num_ratings[product_id] = 1
            last_rating[product_id] = rating.pub_date
        else:
            avg_ratings[product_id] += rating.rating
            num_ratings[product_id] += 1
            if rating.pub_date > last_rating[product_id]:
                last_rating[product_id] = rating.pub_date

    for product_id in avg_ratings:
        avg_ratings[product_id] /= num_ratings[product_id]

    # Tạo DataFrame từ dữ liệu tính toán
    rating_count_df = pd.DataFrame({"avg_rating": avg_ratings, "num_ratings": num_ratings})
    rating_count_df["pub_date"] = pd.Series(last_rating)

    # Kết hợp dữ liệu với thông tin sản phẩm
    product_recs = pd.DataFrame(list(products.values("id")), columns=["id"]).set_index("id").join(rating_count_df)

    # Sắp xếp sản phẩm theo điểm đánh giá trung bình, số lượng đánh giá và ngày đánh giá gần nhất
    ranked_product = product_recs.sort_values(["avg_rating", "num_ratings", "pub_date"], ascending=False)

    # Chuẩn bị dữ liệu để truyền vào template
    context = {"object_list": ranked_product[:15], "title": "List"}

    return render(request, "recommendation.html", context)


@login_required
def detail(request, id):
    product = Product.objects.get()
    reviews = Review.objects.filter(product_id=id)  # Lọc đánh giá của sản phẩm

    # Thực hiện xử lý dữ liệu tại đây
    # results = getFrames(ds)
    # content = recommend(item_id=id, num=6, results=results)

    context = {
        "product": product,
        "reviews": reviews,
    }

    return render(request, "detail.html", context)


@login_required
def post_list(request):
    userId = request.user.id
    userName = request.user.username
    reviews = Review.objects.select_related(
        "product"
    )  # Sử dụng queryset để lấy tất cả đánh giá, kèm theo thông tin sản phẩm

    paginator = Paginator(reviews, 6)
    page = request.GET.get("page")
    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)

    context = {"user_id": userId, "user_name": userName, "object_list": reviews, "title": "List"}
    return render(request, "home.html", context)


@login_required
def get_suggestions(request):
    all_user_names = list(map(lambda x: x, User.objects.only("username")))
    all_product_ids = set(map(lambda x: x.id, Review.objects.only("product")))
    num_users = len(list(all_user_names))
    print(num_users)
    productRatings_m = sp.sparse.dok_matrix((num_users, max(all_product_ids) + 1), dtype=np.float32)
    for i in range(num_users):  # each user corresponds to a row, in the order of all_user_names
        user_reviews = Review.objects.filter(user_name=all_user_names[i])
        for user_review in user_reviews:
            productRatings_m[i, user_review.product.id] = user_review.rating

        productRatings = productRatings_m.transpose()

        coo = productRatings.tocoo(copy=False)
    df = (
        pd.DataFrame({"products": coo.row, "users": coo.col, "rating": coo.data})[["products", "users", "rating"]]
        .sort_values(["products", "users"])
        .reset_index(drop=True)
    )

    mo = df.pivot_table(index=["products"], columns=["users"], values="rating")
    mo.fillna(3, inplace=True)
    model_knn = NearestNeighbors(algorithm="brute", metric="cosine", n_neighbors=7)
    model_knn.fit(mo.values)
    distances, indices = model_knn.kneighbors((mo.iloc[14, :]).values.reshape(1, -1), return_distance=True)
    print(distances, indices)
    print(Product.objects.all())
    username = request.user.username
    print(username)
    context = list(map(lambda x: Product.objects.get(id=indices.flatten()[x]), range(0, len(distances.flatten()))))
    return render(request, "tfidf/cosinesim.html", {"username": request.user.username, "context": context})


# @login_required
# def recommendation(request):
#     if request.user.is_authenticated:
#         # Focus on high-rated products by the user
#         user_reviews = Review.objects.filter(user_name=request.user, rating__gte=4)
#         liked_categories = set(user_reviews.values_list("product__category", flat=True))
#         liked_subcategories = set(user_reviews.values_list("product__subCategory", flat=True))

#         # Recommend based on category, subcategory, and average rating
#         current_recommendations = (
#             Product.objects.filter(Q(category__in=liked_categories) | Q(subCategory__in=liked_subcategories))
#             .exclude(id__in=user_reviews.values_list("product_id", flat=True))  # Exclude already reviewed
#             .order_by("-average_rating", "price")[:10]
#         )  # Prioritize high average ratings

#         context = {"object_list": current_recommendations}
#         return render(request, "recommendation.html", context)
#     else:
#         pass
