from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import Http404
from shop.models import Product, Review
from django.contrib import messages

from django.db.models import Case, When
from .recommendation import Myrecommend
import numpy as np
import pandas as pd


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


def recommend(request):
    if not request.user.is_authenticated:
          return redirect("login")
    if not request.user.is_active:
        raise Http404
    df = pd.DataFrame(list(Review.objects.all().values()))
    print(df)
    nu = df.user_name.unique().shape[0]
    current_user_id = request.user.id
    # if new user not rated any
    # if user_name > nu:
    #     product = Product.objects.get(id=1)
    #     q = Review(user=request.user, product=product, rating=0)
    #     q.save()

    prediction_matrix, Ymean, product_to_row, user_to_column = Myrecommend()
    
    # Lấy user_id từ index của ma trận
    #user_id = list(user_to_column.keys())[list(user_to_column.values()).index(user_id_in_matrix)]
    
    current_user_name = request.user.username
    print(prediction_matrix)
    print(user_to_column)
    name=1
    # Tính toán dự đoán cho user_id_in_matrix
    for key,value in user_to_column.items():
        if key==current_user_name:
           name=value
           break


    my_predictions = prediction_matrix[:, int(name)] + Ymean.flatten()
    print(Ymean.flatten())
    # Sắp xếp dự đoán
    print(my_predictions)
    pred_idxs_sorted = np.argsort(my_predictions)
    pred_idxs_sorted[:] = pred_idxs_sorted[::-1]
    pred_idxs_sorted = pred_idxs_sorted +1

    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pred_idxs_sorted)])

    # Lấy các sản phẩm được dự đoán tốt nhất
    recommended_products = Product.objects.filter(id__in=pred_idxs_sorted[:5]).order_by(preserved)
    print(recommended_products)

    context = {
        'movie_list': recommended_products,
        'user_id': request.user.id,
    }
    print(Ymean)
    return render(request, 'recommend.html', context)

