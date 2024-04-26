from django.contrib import admin
from .models import Wine, Review, Cluster


class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('wine','rating','comment','user_name','pub_date')
    list_filter = ['pub_date','user_name']
    search_fields = ['comment']

class ClusterAdmin(admin.ModelAdmin):
    model = Cluster
    list_display = ['name','get_members']

admin.site.register(Wine)
admin.site.register(Review)
admin.site.register(Cluster)



"""
from django.contrib import admin
from .models import Wine, Review, Cluster

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('wine', 'rating', 'comment', 'user_name', 'pub_date')
    list_filter = ['pub_date', 'user_name']
    search_fields = ['comment']

class ClusterAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_members']

    def get_members(self, obj):
        return "\n".join([u.username for u in obj.users.all()])

    get_members.short_description = 'Members'  # Đổi tên cột

admin.site.register(Wine)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Cluster, ClusterAdmin)
"""