import json
import random

comment = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
    "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
    "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris "
    "nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in "
    "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla "
    "pariatur. Excepteur sint occaecat cupidatat non proident, sunt in "
    "culpa qui officia deserunt mollit anim id est laborum."
)

arr = []


class Review:
    class Fields:
        def __init__(self, product, pub_date, user_name, comment, rating):
            self.product = product
            self.pub_date = pub_date
            self.user_name = user_name
            self.comment = comment
            self.rating = rating

    def __init__(self, product, pub_date, user_name, comment, rating):
        self.model = "shop.Review"
        self.fields = Review.Fields(product, pub_date, user_name, comment, rating).__dict__


for i in range(1, 100):
    # random date
    year = random.randint(2010, 2021)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    date = f"{year}-{month}-{day}"
    product = random.randint(1, 4000)
    rating = random.randint(1, 5)
    review = Review(product, date, f"user{i}", comment, rating)
    arr.append(review.__dict__)

with open("reviews.json", "w") as f:
    json.dump(arr, f)
