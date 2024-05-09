from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views

app_name = "profiles"


urlpatterns = [
    # path('accounts/', include('profiles.accounts.urls', namespace='accounts')),
    # path('profiles/<slug:profile_slug>/change-password', views.change_password, name="change-password"),
    # path('profiles/<slug:profile_slug>/edit', views.edit_profile, name="edit-profile"),
    # path('profiles/<slug:profile_slug>/', views.profile, name="profile"),
    path("<slug:profile_slug>/change-password", views.change_password, name="change-password"),
    path("<slug:profile_slug>/edit", views.edit_profile, name="edit-profile"),
    path("<slug:profile_slug>/", views.profile, name="profile"),
    path("", views.profiles, name="profiles"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
