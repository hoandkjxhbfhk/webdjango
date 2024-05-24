import numpy as np
import pandas as pd
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Case, Q, When
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from shop.models import Product, Review

from .recommendation import Myrecommend, uuCF

# for recommendation
# def recommend(request):
#     if not request.user.is_authenticated:
#         return redirect("login")
#     if not request.user.is_active:
#         raise Http404
#     df = pd.DataFrame(list(Review.objects.all().values()))
#     nu = df.user_name.unique().shape[0]
#     current_user_id = request.user.id
#     # # if new user not rated any movie
#     # if user_name > nu:
#     #     product = Product.objects.get(id=15)
#     #     q = Review(user=request.user, product=product, rating=0)
#     #     q.save()

#     print("Current user id: ", current_user_id)
#     prediction_matrix, Ymean = Myrecommend()
#     print(prediction_matrix)
#     my_predictions = prediction_matrix[:, current_user_id - 1] + Ymean.flatten()
#     pred_idxs_sorted = np.argsort(my_predictions)
#     pred_idxs_sorted[:] = pred_idxs_sorted[::-1]
#     pred_idxs_sorted = pred_idxs_sorted + 1
#     print(pred_idxs_sorted)
#     preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pred_idxs_sorted)])
#     movie_list = list(Product.objects.filter(id__in=pred_idxs_sorted, ).order_by(preserved)[:10])
#     return render(request, 'recommend.html', {'movie_list': movie_list})


# def recommend(request):
#     if not request.user.is_authenticated:
#           return redirect("shop:login")
#     if not request.user.is_active:
#         raise Http404
#     df = pd.DataFrame(list(Review.objects.all().values()))
#     print(df)
#     nu = df.user_name.unique().shape[0]
#     current_user_id = request.user.id
#     # if new user not rated any
#     # if user_name > nu:
#     #     product = Product.objects.get(id=1)
#     #     q = Review(user=request.user, product=product, rating=0)
#     #     q.save()

#     prediction_matrix, Ymean, product_to_row, user_to_column = Myrecommend()

#     # Lấy user_id từ index của ma trận
#     #user_id = list(user_to_column.keys())[list(user_to_column.values()).index(user_id_in_matrix)]

#     current_user_name = request.user.username
#     print(prediction_matrix)
#     print(user_to_column)
#     name=1
#     # Tính toán dự đoán cho user_id_in_matrix
#     for key,value in user_to_column.items():
#         if key==current_user_name:
#            name=value
#            break


#     my_predictions = prediction_matrix[:, int(name)] + Ymean.flatten()
#     print(Ymean.flatten())
#     # Sắp xếp dự đoán
#     print(my_predictions)
#     pred_idxs_sorted = np.argsort(my_predictions)
#     pred_idxs_sorted[:] = pred_idxs_sorted[::-1]


#     preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pred_idxs_sorted)])

#     # Lấy các sản phẩm được dự đoán tốt nhất
#     recommended_products = Product.objects.filter(id__in=pred_idxs_sorted[:5]).order_by(preserved)
#     print(recommended_products)

#     context = {
#         'movie_list': recommended_products,
#         'user_id': request.user.id,
#     }
#     print(Ymean)
#     return render(request, 'recommend.html', context)


def recomend(request):
    if not request.user.is_authenticated:
        return redirect("shop:login")
    if not request.user.is_active:
        raise Http404

    df = pd.DataFrame(list(Review.objects.all().values()))

    # Potential optimization: Load only necessary fields:
    df = pd.DataFrame(list(Review.objects.all().values("user_name", "product_id", "rating")))

    # New user handling (improved)
    user_ratings = df[df["user_name"] == request.user.username]
    if user_ratings.empty:  # If the user has no ratings
        #  Recommendation strategy for new users (explore this further)
        recommended_products = Product.objects.order_by("-name")[:8]  # Placeholder, adjust strategy
    else:
        prediction_matrix, Ymean, product_to_row, user_to_column = Myrecommend()

        current_user_name = request.user.username
        name = user_to_column.get(current_user_name, None)  # Efficient lookup
        if name is None:
            # Handle the case where the user is not in the prediction matrix
            recommended_products = Product.objects.order_by("-name")[:5]  # Placeholder, adjust strategy
        else:
            my_predictions = prediction_matrix[:, int(name)] + Ymean.flatten()
            pred_idxs_sorted = np.argsort(my_predictions)[::-1]
            product_ids = []
            for idx in pred_idxs_sorted[:8]:  # Get top 5
                product_id = list(product_to_row.keys())[list(product_to_row.values()).index(idx)]
                product_ids.append(product_id)

            preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(product_ids)])

            # Lấy các sản phẩm được dự đoán tốt nhất
            recommended_products = Product.objects.filter(id__in=product_ids).order_by(preserved)
            print(recommended_products)
            print(10)
    context = {
        "movie_list": recommended_products,
        "user_id": request.user.id,
    }
    return render(request, "recommend.html", context)


# def recom(request, k=8):
#     user_name = request.user.username
#     all_users = User.objects.all()
#     # Tạo một từ điển để lưu trữ tên người dùng và ID tương ứng
#     user_id_dict = {user.username: user.id for user in all_users}
#     all_reviews = Review.objects.all().values_list("product_id", "user_name", "rating")
#     data_for_uuCF = []
#     product_ids = []
#     for product_id, name, rating in all_reviews:
#         user_id = user_id_dict.get(name)
#         data_for_uuCF.append([user_id, product_id, rating])  # Adjust column order if needed
#         product_ids.append(product_id)  # Store product IDs for later use
#     model = uuCF(data_for_uuCF, k=k)
#     model.fit()

#     predictions = {}
#     for product_id in product_ids:
#         predicted_rating = model.pred(user_id_dict.get(user_name), product_id)
#         predictions[product_id] = predicted_rating

#     # Filter out already rated products
#     user_reviews = Review.objects.filter(user_name=user_name).values_list("product_id", flat=True)
#     already_rated_product_ids = set(user_reviews)

#     # Sort and select top-k recommendations
#     recommendations = []
#     for product_id, predicted_rating in predictions.items():
#         if product_id not in already_rated_product_ids:
#             recommendations.append((product_id, predicted_rating))
#     recommendations.sort(key=lambda x: x[1], reverse=True)  # Sort by predicted rating
#     top_k_recommendations = recommendations[:k]


#     # Retrieve recommended products
#     recommended_product_ids = [rec[0] for rec in top_k_recommendations]
#     recommended_products = Product.objects.filter(id__in=recommended_product_ids)
#     context = {
#         "movie_list": recommended_products,
#         "user_id": request.user.id,
#     }
#     return render(request, "recommend.html", context)
def recom(request, k=8):
    user_name = request.user.username
    all_users = User.objects.all()
    # Tạo một từ điển để lưu trữ tên người dùng và ID tương ứng
    user_id_dict = {user.username: user.id for user in all_users}
    all_reviews = Review.objects.all().values_list("product_id", "user_name", "rating")

    # Check if all_reviews is empty
    if not all_reviews:
        # No reviews, return the first 8 products
        recommended_products = Product.objects.all()[:k]
        context = {
            "movie_list": recommended_products,
            "user_id": request.user.id,
        }
        return render(request, "recommend.html", context)

    data_for_uuCF = []
    product_ids = []
    for product_id, name, rating in all_reviews:
        user_id = user_id_dict.get(name)
        data_for_uuCF.append([user_id, product_id, rating])  # Adjust column order if needed
        product_ids.append(product_id)  # Store product IDs for later use

    model = uuCF(data_for_uuCF, k=k)
    model.fit()

    predictions = {}
    for product_id in product_ids:
        predicted_rating = model.pred(user_id_dict.get(user_name), product_id)
        predictions[product_id] = predicted_rating

    # Filter out already rated products
    user_reviews = Review.objects.filter(user_name=user_name).values_list("product_id", flat=True)
    already_rated_product_ids = set(user_reviews)

    # Sort and select top-k recommendations
    recommendations = []
    for product_id, predicted_rating in predictions.items():
        if product_id not in already_rated_product_ids:
            recommendations.append((product_id, predicted_rating))
    recommendations.sort(key=lambda x: x[1], reverse=True)  # Sort by predicted rating
    top_k_recommendations = recommendations[:k]

    # Retrieve recommended products
    recommended_product_ids = [rec[0] for rec in top_k_recommendations]
    recommended_products = Product.objects.filter(id__in=recommended_product_ids)
    context = {
        "movie_list": recommended_products,
        "user_id": request.user.id,
    }
    return render(request, "recommend.html", context)
