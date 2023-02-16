from django.contrib import admin
from django.contrib.auth.models import Group
from orders.models import Place, DevicesService, SnacksService, Quantity, Order


admin.site.unregister(Group)
admin.site.register(DevicesService)
admin.site.register(SnacksService)
admin.site.register(Place)


class QuantityReview(admin.TabularInline):
    model = Quantity
    extra = 0


@admin.register(Order)
class EventAdmin(admin.ModelAdmin):
    inlines = [QuantityReview]
    model = Order
    search_fields = ['place__name']
    list_display = [
        "place",
        "start",
        "end",
        "is_active",
        "is_deleted",
    ]
    list_filter = ["is_active", "is_deleted"]
