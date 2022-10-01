from django.contrib import admin

# from app.forms import UserAdminAuthenticationForm
from myFinance.models import Transaction, Tag, DateInput, TransactionNameTag, TagGoal, Credential, AdditionalInfo


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'month', 'date', 'tag', 'month_date', 'bank', 'arn')

    class Meta:
        model = Transaction


@admin.register(TagGoal)
class TagGoalAdmin(admin.ModelAdmin):
    list_display = ('user', 'tag', 'value',)

    class Meta:
        model = TagGoal


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'expense')

    class Meta:
        model = Tag


@admin.register(DateInput)
class DateInputAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')

    class Meta:
        model = DateInput


@admin.register(TransactionNameTag)
class TransactionNameTagAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_name', 'tag')

    class Meta:
        model = TransactionNameTag


@admin.register(Credential)
class CredentialAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'last_scanned')
    readonly_fields = ('user',)
    exclude = ('credential',)

    class Meta:
        model = Credential


@admin.register(AdditionalInfo)
class AdditionalInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at', 'value')
    readonly_fields = ('user',)

    class Meta:
        model = AdditionalInfo


# -------------------------------------------------------------------------
from .models import Transaction
from django.contrib.admin import AdminSite


class UserAdminSite(AdminSite):
    site_header = 'Monty Python administration'

    # login_form = UserAdminAuthenticationForm
    def has_permission(self, request):
        """
        Removed check for is_staff.
        """
        return request.user.is_active


class BaseAdminModel(admin.ModelAdmin):
    def get_queryset(self, request):
        """Limit Pages to those that belong to the request's user."""
        qs = super(BaseAdminModel, self).get_queryset(request)
        # if request.user.is_superuser:
        #     # It is mine, all mine. Just return everything.
        #     return qs
        # Now we just add an extra filter on the queryset and
        # we're done. Assumption: Page.owner is a foreignkey
        # to a User.
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


class TransactionMyAdmin(BaseAdminModel):
    list_display = ('name', 'value', 'month', 'date', 'tag', 'month_date')

    readonly_fields = ('user',)


class TagMyAdmin(BaseAdminModel):
    list_display = ('name',)
    readonly_fields = ('user',)


class DateMyAdmin(BaseAdminModel):
    list_display = ('name', 'date')
    readonly_fields = ('user',)

    class Meta:
        model = DateInput


admin_site = UserAdminSite(name='myadmin')
admin_site.register(Transaction, TransactionMyAdmin)
admin_site.register(Tag, TagMyAdmin)
admin_site.register(DateInput, DateMyAdmin)
