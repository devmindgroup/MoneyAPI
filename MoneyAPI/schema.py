# schema.py
from ninja import Schema
from typing import Optional


class BankServerSchema(Schema):
    id: int
    name: str
    server_ip_address: str

    class Config:
        orm_mode = True


from ninja import Schema
from typing import Optional

# BankServer schema
class BankServerSchema(Schema):
    id: int
    name: str  # Add other fields as necessary

    class Config:
        orm_mode = True

# Input schema
class BankAccountCreateSchema(Schema):
    bank_server: int  # ID of the associated BankServer
    account_name: str
    account_number: str

# Output schema
class BankAccountSchema(Schema):
    id: int
    bank_server: BankServerSchema  # Use nested schema for bank_server
    account_name: str
    account_number: str

    class Config:
        orm_mode = True


# Transaction schemas
class TransactionSchema(Schema):
    id: int
    transaction_type: str  # 'BANK' or 'MOBILE'
    amount: float
    source_account: BankAccountSchema  # Nested schema for detailed account info
    target_iban: Optional[str] = None
    target_swift_code: Optional[str] = None
    target_bank_account_number: Optional[str] = None
    target_bank_name: Optional[str] = None
    target_phone_number: Optional[str] = None
    target_country: Optional[str] = None
    provider: Optional[str] = None
    status: str  # 'pending', 'success', 'failed'
    created_at: str  # DateTime in ISO format

    class Config:
        orm_mode = True

    @staticmethod
    def from_transaction(transaction):
        """
        Convert a Transaction model instance to a TransactionSchema instance.
        Ensures datetime is serialized as ISO strings.
        """
        return TransactionSchema(
            id=transaction.id,
            transaction_type=transaction.transaction_type,
            amount=transaction.amount,
            source_account=BankAccountSchema.from_orm(transaction.source_account),
            target_iban=transaction.target_iban,
            target_swift_code=transaction.target_swift_code,
            target_bank_account_number=transaction.target_bank_account_number,
            target_bank_name=transaction.target_bank_name,
            target_phone_number=transaction.target_phone_number,
            target_country=transaction.target_country,
            provider=transaction.provider,
            status=transaction.status,
            created_at=transaction.created_at.isoformat(),
        )


class TransactionCreateSchema(Schema):
    transaction_type: str  # 'BANK' or 'MOBILE'
    amount: float
    source_account: int  # ID of the source BankAccount
    target_iban: Optional[str] = None
    target_swift_code: Optional[str] = None
    target_bank_account_number: Optional[str] = None
    target_bank_name: Optional[str] = None
    target_phone_number: Optional[str] = None
    target_country: Optional[str] = None
    provider: Optional[str] = None

    class Config:
        orm_mode = True


class TransactionStatusUpdateSchema(Schema):
    status: str  # 'pending', 'success', 'failed'

    class Config:
        orm_mode = True