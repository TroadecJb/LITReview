from django.contrib import admin

from .models import Review, Ticket

class ReviewAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Headline Review", {"fields": ["headline", "user"]}),
        ("other", {"fields": ["rating", "body","ticket"]}),
    ]
    list_display = ["headline", "user", "time_created"]

class TicketAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Title Ticket", {"fields": ["title", "user"]}),
        ("Other", {"fields": ["description", "image", "available"]}),
    ]
    list_display = ["title", "user", "time_created", "available"]


admin.site.register(Review, ReviewAdmin)
admin.site.register(Ticket, TicketAdmin)