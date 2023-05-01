from django.urls import path

from . import views

app_name = "follow_sys"

urlpatterns = [
    path("follow/", views.Subscriptions.as_view(), name="subscriptions"),
    path(
        "follow/followed_user_id_<int:followed_user_id>/delete/",
        views.DeleteSubscription.as_view(),
        name="delete-subscription",
    ),
]
