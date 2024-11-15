# models.py
from django.db import models
from uuid import uuid4

class BankServer(models.Model):
    """Represents a commercial bank's server."""
    name = models.CharField(max_length=100, unique=True)       # e.g., "Chase Bank"
    server_ip_address = models.GenericIPAddressField(unique=True)

    def __str__(self):
        return self.name


class BankAccount(models.Model):
    """Represents an individual bank account under a BankServer."""
    bank_server = models.ForeignKey(BankServer, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=50)
    account_number = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.account_name} - {self.account_number}"


class Transaction(models.Model):
    """Records each transaction (mobile money or bank transfer) with necessary details."""
    TRANSACTION_TYPES = [
        ('BANK', 'Bank Transfer'),
        ('MOBILE', 'Mobile Money Transfer')
    ]
    TRANSACTION_STATUSES = [
        ('pending', 'pending'),
        ('success', 'success'),
        ('failed', 'failed'),
    ]
    
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    source_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name="transactions")
    
    # Target information for bank transfers
    target_iban = models.CharField(max_length=34, blank=True, null=True)          # IBAN for international transfers
    target_swift_code = models.CharField(max_length=11, blank=True, null=True)     # SWIFT code for international banks
    target_bank_account_number = models.CharField(max_length=20, blank=True, null=True)  # Bank account number
    target_bank_name = models.CharField(max_length=100, blank=True, null=True)     # Name of the bank receiving the funds
    
    # Target information for mobile money transfers
    target_phone_number = models.CharField(max_length=15, blank=True, null=True)   # Mobile number for mobile money transfers
    target_country = models.CharField(max_length=50, blank=True, null=True)        # Country for mobile money transfers
    provider = models.CharField(max_length=50, blank=True, null=True)              # Mobile money provider (e.g., Airtel, MTN)

    status = models.CharField(max_length=20, default='Pending', choices=TRANSACTION_STATUSES, editable=True)                    # Transaction status
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} - {self.status}"



class APIKey(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    api_key = models.UUIDField(unique=True, editable=False, default=uuid4())

