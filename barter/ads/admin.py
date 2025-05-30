from django.contrib import admin
from .models import Ad, ExchangeProposal, Category


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'category', 'condition', 'created_at')
    list_filter = ('category', 'condition', 'created_at')
    search_fields = ('title', 'description', 'user__username')


@admin.register(ExchangeProposal)
class ExchangeProposalAdmin(admin.ModelAdmin):
    list_display = ('id', 'ad_sender', 'ad_receiver', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('ad_sender__title', 'ad_receiver__title', 'comment')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
