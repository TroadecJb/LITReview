from django import forms
from . import models


class FollowUserForm(forms.ModelForm):
    class Meta:
        model = models.UserFollows
        fields = ["user", "followed_user"]
        widgets = {
            "followed_user": forms.TextInput(attrs={"placeholder": "Username"})
        }
