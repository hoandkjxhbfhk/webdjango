from django.conf import settings
from django.urls import include, path

from . import views

app_name = "shop"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("about/", views.about, name="about"),
    path("", include("django.contrib.auth.urls")),
    # path('oauth/', include('social_django.urls', namespace="social")),
    path("product_list_category/", views.index, name="list"),
    path("index/", views.index, name="index"),
    path("product_list", views.index, name="product_list"),
    path("search/", views.search_list, name="query"),
    # path('trending/', views.search_list, name ='query'),
    path("product_detail/<int:id>/<slug:slug>/", views.product_detail, name="product_detail"),
    path(
        "product_list_by_subcategory/<slug:subcategory_slug>/",
        views.product_list_subcategory,
        name="product_list_by_subcategory",
    ),
    path("reviewlist/", views.review_list, name="review_list"),
    path("review/<int:review_id>/", views.review_detail, name="review_detail"),
    path("product/", views.product_list, name="product_list"),
    path("product/<int:product_id>/", views.product_detail, name="product_detail"),
    path("product/<int:product_id>/add_review/", views.add_review, name="add_review"),
    path("review/user/<str:username>/", views.user_review_list, name="user_review_list"),
    path("review/user/", views.user_review_list, name="user_review_list"),
    path("recommendation/", views.user_recommendation_list, name="user_recommendation_list"),
    path("product_list_by_category/<slug:category_slug>/", views.index, name="product_list_by_category"),
]

if settings.DEBUG:
    print("URL Patterns:")
    for pattern in urlpatterns:
        print(pattern)  # Or use sophisticated logging
