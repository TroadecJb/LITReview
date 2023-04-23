from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.core.paginator import Paginator
from django.views import generic
from itertools import chain

from follow_sys.models import UserFollows
from .models import Review, Ticket, RATING_RANGE, RATING_OFF, RATING_ON
from .forms import ReviewForm, TicketForm, DeletePostForm

@login_required
def feed(request):
    ### Return every ticket available and made by the user, every review made by the user or users they follow.
    ###
    reviews = Review.objects.filter(
        user__in=[user_follow.followed_user for user_follow in UserFollows.objects.filter(user=request.user)]
    )
    tickets = Ticket.objects.filter(
        Q(available=True) | Q(user=request.user)
    )
    
    content = sorted(
        chain(reviews, tickets), key=lambda i: i.time_created, reverse=True
    )

    paginator = Paginator(content, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "rating_range": RATING_RANGE,
        "rating_on": RATING_ON,
        "rating_off": RATING_OFF
    }
    return render(request, "publications/feed.html", context=context)

@login_required
def selfPosts(request):
    ### Return every ticket and review made by the user.
    ###
    reviews = Review.objects.filter(
        Q(user=request.user)
    )
    tickets = Ticket.objects.filter(
        Q(user=request.user)
    )

    content = sorted(chain(reviews, tickets), key=lambda i: i.time_created, reverse=True)

    paginator = Paginator(content, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
    }

    return render(request, "publications/posts.html", context=context)

@login_required
def ViewReview(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    return render(request, "publications/review.html", {"review": review})

@login_required
def ViewTicket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, "publications/ticket.html", {"ticket": ticket})

@method_decorator(login_required, name="dispatch")
class CreateReview(generic.DetailView):
    ### Complete Review creation form (ticket + review)
    ###
    model = Review

    def get(self, request):
        ### Ticket and Review creation forms to create a complete Review.
        ###
        review_form = ReviewForm()
        ticket_form = TicketForm()

        context = {
            "ticket_form": ticket_form,
            "review_form": review_form,
        }
        return render(request, "publications/create_review.html", context=context)
        

    def post(self, request):
        ### Ticket and Review creation froms validation.
        ###
        review_form = ReviewForm(request.POST)
        ticket_form = TicketForm(request.POST, request.FILES)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.available = False
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("publications:feed")
        
        context = {
            "ticket_form": ticket_form,
            "review_form": review_form,
        }

        return render(request, "publications/create_review.html", context=context)
        
@method_decorator(login_required, name="dispatch")
class CreateReviewFromTicket(generic.DetailView):
    ### Review creation form from another user ticket.
    ###
    model = Review
    template_name = "publications/create_review.html"

    def get(self, request, ticket_id):
        ### Display ticket and the review creation form.
        ###
        review_form = ReviewForm()
        ticket = get_object_or_404(Ticket, id=ticket_id)

        context = {
            "ticket": ticket,
            "review_form": review_form,
        }
        return render(request, "publications/create_reply_review.html", context=context)
        

    def post(self, request, ticket_id):
        ### Check review form validity and make ticket unavailable.
        ###
        review_form = ReviewForm(request.POST)
        ticket = get_object_or_404(Ticket, id=ticket_id)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            ticket.available = False
            ticket.save()
            return redirect("publications:feed")

@method_decorator(login_required, name="dispatch")
class CreateTicket(generic.DetailView):
    ### Ticket creation form.
    ###
    model = Ticket
    template_name = "publications/ticket.html"

    def get(self, request):
        ticket_form =TicketForm()

        context = {
            "ticket_form": ticket_form,
        }
        return render(request, "publications/create_ticket.html", context=context)
    
    def post(self, request):
        ticket_form = TicketForm(request.POST, request.FILES)

        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("publications:feed")

@method_decorator(login_required, name="dispatch")
class EditReview(generic.DetailView):
    ### Review edit form. Check if user is also the author of the ticket, if user is the author the form allows to ticket edit too.
    ###
    model = Review

    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        ticket = get_object_or_404(Ticket, id=review.ticket.id)

        if request.user == review.user and request.user == ticket.user:
            edit_review_form = ReviewForm(instance=review)
            edit_ticket_from = TicketForm(instance=ticket)
            delete_from = DeletePostForm()

            context = {
                "edit_review_form": edit_review_form,
                "edit_ticket_form": edit_ticket_from,
                "delete_form": delete_from,
            }

            return render(request, "publications/edit_ticket_review.html", context=context)
        
        elif request.user == review.user and request.user != ticket.user:
            edit_review_form = ReviewForm(instance=review)
            delete_from = DeletePostForm()

            context = {
                "edit_review_form": edit_review_form,
                "delete_form": delete_from,
            }

            return render(request, "publications/edit_review.html", context=context)
    
    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        ticket = get_object_or_404(Ticket, id=review.ticket.id)
        edit_review_form = ReviewForm(instance=review)
        edit_ticket_from = TicketForm(instance=ticket)
        delete_form = DeletePostForm()
        
        if "edit_review" in request.POST:
            if request.user == review.user and request.user == ticket.user:
                edit_review_form = ReviewForm(request.POST, instance=review)
                edit_ticket_from = TicketForm(request.POST, request.FILES, instance=ticket)
                
                if all([edit_review_form.is_valid(), edit_ticket_from.is_valid()]):
                    edit_ticket_from.save()
                    edit_review_form.save()
                
                    return redirect("publications:feed")
            
            elif request.user == review.user and request.user != ticket.user:
                edit_review_form = ReviewForm(request.POST, instance=review)
                
                if edit_review_form.is_valid():
                    edit_review_form.save()
                
                    return redirect("publications:feed")
        
        elif "delete_post" in request.POST:
            delete_form = DeletePostForm(request.POST)
            if delete_form.is_valid():
                ticket.available = True
                review.delete()
                return redirect("publications:feed")


@method_decorator(login_required, name="dispatch")     
class EditTicket(generic.DetailView):
    ### Ticket edit form.
    ###
    model = Ticket

    def get(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        if request.user == ticket.user:
            edit_ticket_form = TicketForm(instance=ticket)
            delete_form = DeletePostForm()

            context = {
                "edit_ticket_form": edit_ticket_form,
                "delete_form": delete_form,
            }

            return render(request, "publications/edit_ticket.html", context=context)
        return redirect("publications:feed")

    def post(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        if request.user == ticket.user:
            if "edit_ticket" in request.POST:
                edit_ticket_form = TicketForm(request.POST, request.FILES, instance=ticket)

                if edit_ticket_form.is_valid():
                    edit_ticket_form.save()
                    return redirect("publications:feed")
            
            elif "delete_post" in request.POST:
                delete_form = DeletePostForm(request.POST)
                if delete_form.is_valid():
                    ticket.delete()
                    return redirect("publications:feed")

        return redirect("publications:feed")