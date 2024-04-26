from django.test import TestCase


"""
from django.test import TestCase
from .models import Wine, Review, Cluster
from django.contrib.auth.models import User

class YourAppNameTestCase(TestCase):
    
    def setUp(self):
        # Tạo các đối tượng cho các bài kiểm tra
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.wine1 = Wine.objects.create(name='Wine 1')
        self.wine2 = Wine.objects.create(name='Wine 2')
        Review.objects.create(user_name='user1', wine=self.wine1, rating=4)
        Review.objects.create(user_name='user2', wine=self.wine1, rating=5)

    def test_average_rating(self):
        # Kiểm tra phương thức average_rating của đối tượng Wine
        wine1 = Wine.objects.get(name='Wine 1')
        self.assertEqual(wine1.average_rating(), 4.5)

    def test_cluster_creation(self):
        # Kiểm tra tạo cụm
        Cluster.objects.create(name='Test Cluster')
        self.assertEqual(Cluster.objects.count(), 1)

    def test_cluster_member_count(self):
        # Kiểm tra số lượng thành viên trong cụm
        cluster = Cluster.objects.create(name='Test Cluster')
        cluster.users.add(self.user1)
        cluster.users.add(self.user2)
        self.assertEqual(cluster.get_member_count(), 2)

    # Bổ sung các bài kiểm tra khác nếu cần thiết


"""
