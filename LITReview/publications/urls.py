from django.urls import path

from . import views

app_name = "publications"

urlpatterns = [
    path("feed/", views.feed, name="feed"),
    path("review/<int:review_id>/", views.ViewReview, name="review"),
    path("review/<int:review_id>/edit/", views.EditReview.as_view(), name="edit-review"),
    path("review/<int:review_id>/delete/", views.ReviewDeleteConfirmation.as_view(), name="delete-review"),
    path("review/create/", views.CreateReview.as_view(), name="create-review"),
    path("ticket/<int:ticket_id>/", views.ViewTicket, name="ticket"),
    path("ticket/<int:ticket_id>/edit/", views.EditTicket.as_view(), name="edit-ticket"),
    path("ticket/<int:ticket_id>/delete/", views.TicketDeleteConfirmation.as_view(), name="delete-ticket"),
    path("ticket/<int:ticket_id>/reply/", views.CreateReviewFromTicket.as_view(), name="create-review-ticket"),
    path("ticket/create/", views.CreateTicket.as_view(), name="create-ticket"),
    path("posts/", views.selfPosts, name="posts"),
    
    
]