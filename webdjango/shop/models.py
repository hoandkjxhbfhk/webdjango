import numpy as np
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

ADDRESS_CHOICES = (
    ("B", "Billing"),
    ("S", "Shipping"),
)
District_choices = (
    ("D", "Dang"),
    ("S", "Shipping"),
)


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    image = models.ImageField(upload_to="category/", blank=True)

    class Meta:
        db_table = "category"
        ordering = ("name",)
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:product_list_by_category", args=[self.slug])


class SubCategory(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    image = models.ImageField(upload_to="subcategory/", blank=True)

    class Meta:
        db_table = "subcategory"
        ordering = ("name",)
        verbose_name = "subcategory"
        verbose_name_plural = "subcategories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:product_list_by_subcategory", args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    subCategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True, max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.PositiveIntegerField()
    discount_price = models.FloatField(blank=True, null=True)
    # pub_date = models.DateField()
    stock = models.PositiveIntegerField(default=100)
    available = models.BooleanField(default=True)
    # created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super(Product, self).__init__(*args, **kwargs)
        if self.price:
            self.discount_price = self.price * 0.9

    class Meta:
        # ordering = ('-created',)
        index_together = (("id", "slug"),)

    def average_rating(self):
        all_ratings = list(map(lambda x: x.rating, self.review_set.all()))
        return np.mean(all_ratings)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "shop:product_detail",
            args=[
                self.id,
            ],
        )
        # return reverse('product_detail', args=[self.id,])


class Slider(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to="slider", blank=True)
    description = models.CharField(max_length=200, db_index=True)

    class Meta:
        db_table = "slider"
        ordering = ("name",)
        verbose_name = "slider"
        verbose_name_plural = "sliders"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:slider", args=[self.name, self.slug])


# for reccomednation part

# class Wine(models.Model):
#         name = models.CharField(max_length=200)
#
#         def average_rating(self):
#             all_ratings = list(map(lambda x: x.rating, self.review_set.all()))
#             return np.mean(all_ratings)
#
#         def __unicode__(self):
#             return self.name


class Review(models.Model):
    RATING_CHOICES = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    )
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    pub_date = models.DateTimeField("ngày tạo")
    user_name = models.CharField(max_length=100)
    comment = models.CharField(max_length=2000)
    rating = models.IntegerField(choices=RATING_CHOICES)


class Cluster(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User, related_name="shop_clusters")

    def get_members(self):
        return "\n".join([u.username for u in self.users.all()])
