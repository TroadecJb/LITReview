from django import forms
from .models import Review, Ticket


class ReviewForm(forms.ModelForm):
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]
        widgets = {
            "rating": forms.RadioSelect(
                choices=[
                    (0, "0"),
                    (1, "1"),
                    (2, "2"),
                    (3, "3"),
                    (4, "4"),
                    (5, "5"),
                ]
            )
        }


class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]


class DeletePostForm(forms.Form):
    delete_post = forms.BooleanField(widget=forms.HiddenInput, initial=True)
