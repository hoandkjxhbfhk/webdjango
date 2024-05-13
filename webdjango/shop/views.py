import datetime
import json
import random

import numpy as np
import pandas as pd
from django.contrib import auth, messages
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.text import slugify
from order.models import ShopCartForm
from profiles.models import Profile

from .forms import ReviewForm
from .models import Category, Cluster, Product, Review, Slider, SubCategory
from .suggestions import update_clusters


def signup(request):
    if request.method == "POST":
        # creating a user
        if request.POST["password"] == request.POST["repeatpassword"]:
            try:
                user = User.objects.get(username=request.POST["username"])
                return render(request, "Register.html", {"error": " Tài khoản đã tồn tại "})
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=request.POST["username"], password=request.POST["password"], email=request.POST["email"]
                )

                # Tạo Profile mới
                email = request.POST["email"]
                username = request.POST["username"]
                Profile.objects.create(user=user, first_name=username, email=email)  # Tạo profile cho người dùng mới
                

                return redirect("shop:index")
        else:
            return render(request, "Register.html", {"error": " Mật khẩu không khớp "})

    else:
        return render(request, "Register.html")


# def signup(request):
#     if request.method == "POST":
#         # creating a user
#         if request.POST['password'] == request.POST['repeatpassword']:
#             try:
#                 user = User.objects.get(username=request.POST['username'])
#                 return render(request, 'Register.html', {'error': "User already exist"})
#             except User.DoesNotExist:
#                 user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'],
#                                                 email=request.POST['email'])

#                 return redirect("shop:index")
#         else:
#             return render(request, 'Register.html', {'error': "Password Don't match"})

#     else:
#         return render(request, 'Register.html')


def user_login(request):
    if request.method == "POST":
        uname = request.POST["username"]
        pwd = request.POST["password"]
        user = auth.authenticate(username=uname, password=pwd)
        if user is not None:
            auth.login(request, user)
            # return render(request, 'index.html', {'error': "Invalid Login"})
            return redirect("shop:index")

        else:
            return render(request, "login.html", {"error": "Invalid Login "})
    else:
        update_clusters(True)
        return render(request, "login.html")


def user_logout(request):
    logout(request)
    return redirect("shop:index")


def index(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    slider = Slider.objects.all()
    products = Product.objects.filter(available=True).order_by("-name")

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)  # Filter first

    paginator = Paginator(products, 20)  # Paginate the filtered set
    page = request.GET.get("page")
    paged_products = paginator.get_page(page)

    # Calculate the range of page numbers to display
    if paged_products.number <= 5:
        page_range = range(1, min(11, paginator.num_pages + 1))
    elif paged_products.number >= paginator.num_pages - 5:
        page_range = range(max(1, paginator.num_pages - 10), paginator.num_pages + 1)
    else:
        page_range = range(paged_products.number - 5, paged_products.number + 6)

    context = {
        "category": category,
        "categories": categories,
        "slider": slider,
        "electronics": {},
        "product_list": products,
        "products": paged_products,  # Pass the paginated results
        "page_range": page_range,
    }

    return render(request, "index.html", context)


def about(request, category_slug=None):
    category = None
    categories = Category.objects.filter(Q(name="sweate"))
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, "about.html", {"category": category, "categories": categories, "products": products})


def search_list(request):
    print(request.GET)
    method_dir = request
    query = method_dir.GET.get("q", None)
    if query is not None:
        lookups = Q(name=query) | Q(description=query)
        products = Product.objects.filter(lookups).distinct()
    else:
        products = Product.objects.none()

    print(products)

    return render(request, "searchview.html", {"products": products})



def product_list_subcategory(request, subcategory_slug=None):
    subcategories = SubCategory.objects.all()
    products = Product.objects.filter(available=True)
    if subcategory_slug:
        subcategory = get_object_or_404(SubCategory, slug=subcategory_slug)
        print(subcategory)
        products = products.filter(subCategory=subcategory)
    return render(
        request, "list.html", {"subcategory": subcategory, "subcategories": subcategories, "products": products}
    )


# def product_detail(request, id, slug):
#     product = get_object_or_404(Product, id=id, slug=slug, available=True)
#     # cart_product_form = CartAddProductForm()
#     return render(request,
#                   'shop/show.html',
#                   {'product': product})


# for recommendation


def review_list(request):
    latest_review_list = Review.objects.order_by("-pub_date")[:9]
    context = {"latest_review_list": latest_review_list}
    return render(request, "review_list.html", context)


def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, "review_detail.html", {"review": review})


def product_list(request):
    product_list = Product.objects.all()
    context = {"product_list": product_list}
    return render(request, "product_list.html", context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    form = ShopCartForm()

    user_reviews = Review.objects.filter(user_name=request.user.username).prefetch_related("product")
    user_reviews_product_ids = set(map(lambda x: x.product.id, user_reviews))

    # get request user cluster name (just the first one right now)
    try:
        user_cluster_name = User.objects.get(username=request.user.username).cluster_set.first().name
    except:  # if no cluster assigned for a user, update clusters
        update_clusters(is_new_user=True)
        user_cluster_name = User.objects.get(username=request.user.username).cluster_set.first().name

    # get usernames for other memebers of the cluster
    user_cluster_other_members = (
        Cluster.objects.get(name=user_cluster_name).users.exclude(username=request.user.username).all()
    )
    other_members_usernames = set(map(lambda x: x.username, user_cluster_other_members))

    # get reviews by those users, excluding product reviewed by the request user
    other_users_reviews = Review.objects.filter(user_name__in=other_members_usernames).exclude(
        product__id__in=user_reviews_product_ids
    )
    other_users_reviews_product_ids = set(map(lambda x: x.product.id, other_users_reviews))

    # then get a product list including the previous IDs, order by rating
    product_list = sorted(
        list(Product.objects.filter(id__in=other_users_reviews_product_ids)),
        key=lambda x: x.average_rating(),
        reverse=True,
    )
    product_list=product_list[:4]
    print(product_list)


    return render(request, "product_detail.html", {"product": product, "form": form, "product_list": product_list})


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data["rating"]
        comment = form.cleaned_data["comment"]
        user_name = request.user.username
        review = Review()
        review.product = product
        review.user_name = user_name
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        update_clusters(is_new_user=False)

        return HttpResponseRedirect(reverse("shop:product_detail", args=(product.id,)))

    return render(request, "product_detail.html", {"product": product, "form": form})


def user_review_list(request, username=None):
    if not username:
        username = request.user.username
    latest_review_list = Review.objects.filter(user_name=username).order_by("-pub_date")
    context = {"latest_review_list": latest_review_list, "username": username}
    return render(request, "user_review_list.html", context)


@login_required
def user_recommendation_list(request):
    # get request user reviewed products
    user_reviews = Review.objects.filter(user_name=request.user.username).prefetch_related("product")
    user_reviews_product_ids = set(map(lambda x: x.product.id, user_reviews))

    # get request user cluster name (just the first one right now)
    try:
        user_cluster_name = User.objects.get(username=request.user.username).cluster_set.first().name
    except:  # if no cluster assigned for a user, update clusters
        update_clusters(is_new_user=True)
        user_cluster_name = User.objects.get(username=request.user.username).cluster_set.first().name

    # get usernames for other memebers of the cluster
    user_cluster_other_members = (
        Cluster.objects.get(name=user_cluster_name).users.exclude(username=request.user.username).all()
    )
    other_members_usernames = set(map(lambda x: x.username, user_cluster_other_members))

    # get reviews by those users, excluding product reviewed by the request user
    other_users_reviews = Review.objects.filter(user_name__in=other_members_usernames).exclude(
        product__id__in=user_reviews_product_ids
    )
    other_users_reviews_product_ids = set(map(lambda x: x.product.id, other_users_reviews))

    # then get a product list including the previous IDs, order by rating
    product_list = sorted(
        list(Product.objects.filter(id__in=other_users_reviews_product_ids)),
        key=lambda x: x.average_rating(),
        reverse=True,
    )

    return render(request, "recommend.html", {"username": request.user.username, "movie_list": product_list})
