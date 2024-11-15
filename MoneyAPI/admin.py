from django.contrib import admin
from .models import *


admin.AdminSite.site_header = 'Money Transfer API'
admin.AdminSite.index_title = '''
Welcome To Money Transfer API Portal. This API serves as a robust platform for sending funds to
mobile wallets as well as banks across the world using API calls. This API works with any bank
network for all banks.
'''

@admin.register(BankServer)
class BankServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'server_ip_address')
    search_fields = ('name', 'server_ip_address')
    list_filter = ('name',)


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('account_name', 'account_number', 'bank_server')
    search_fields = ('account_name', 'account_number', 'bank_server__name')
    list_filter = ('bank_server',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'transaction_type', 'amount', 'source_account', 
        'target_bank_name', 'target_phone_number', 'provider', 
        'status', 'created_at'
    )
    search_fields = (
        'source_account__account_name', 'target_bank_account_number', 
        'target_phone_number', 'target_bank_name'
    )
    list_filter = ('transaction_type', 'status', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = [
        'api_key', 'created_at', 'updated_at'
    ]