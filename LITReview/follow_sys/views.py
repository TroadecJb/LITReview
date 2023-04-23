from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.models import User
from urllib.parse import urlencode
from .forms import FollowUserForm
from .models import UserFollows


class Subscriptions(generic.ListView):
    template_name = "follow_sys/follow.html"

    def get(self, request):
        ### List of all subscriptions the user have and has made ###
        follow_form = FollowUserForm()
        current_user = request.user
        subscriptions = list(UserFollows.objects.filter(user=current_user))
        subscribers = [
            sub.user for sub in UserFollows.objects.filter(followed_user=current_user)
        ]

        context = {
            "follow_form": follow_form,
            "subscriptions": subscriptions,
            "subscribers": subscribers,
        }

        return render(request, "follow_sys/follow.html", context=context)
    
    def post(self, request):
        ### Add a new subscription, prevent self susbcriptions and non exisiting user ###
        current_user = request.user
        followed_user_username = request.POST.get("followed_user")

        if User.objects.filter(username=followed_user_username).exists() and followed_user_username != request.user.username:
            followed_user_id = User.objects.get(
                username=followed_user_username
            ).id
            follow_form = FollowUserForm(
                {"user": current_user, "followed_user": followed_user_id}
            )

            if follow_form.is_valid():
                follow_form.save()

        return redirect("follow_sys:subscriptions")

class DeleteSubscription(generic.DetailView):
    
    def get(self, request, followed_user_id):
        ### Remove from the subscriptions list the user ###
        current_user = request.user
        followed_user = User.objects.get(id=followed_user_id)
        sub_to_delete = UserFollows.objects.get(
            user=current_user, followed_user=followed_user
        )
        sub_to_delete.delete()        

        return redirect("follow_sys:subscriptions")