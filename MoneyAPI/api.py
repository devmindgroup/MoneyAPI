from ninja import NinjaAPI, Redoc
from typing import List
from .models import BankServer, BankAccount, Transaction
from .schema import *
from django.shortcuts import get_object_or_404

from ninja.security import HttpBearer

class ApiKey(HttpBearer):
    def authenticate(self, request, token):
        if token == "47061d41-7994-4fad-99a7-54879acd9a83":
            return token
        return None
    


api = NinjaAPI(
    title="Money API - Server to Server API Transfer - Crypto Flash - USDT, BTC, ETH, e.t.c",
    description="""
    Crypto Flash API Documentation
    ===============================

    The Crypto Flash API is a robust and versatile solution designed to facilitate seamless transactions 
    across various cryptocurrencies, including USDT, BTC, ETH, and more. In addition to cryptocurrency operations, 
    this API enables direct transfers of funds to bank accounts globally.

    The API offers server-to-server communication capabilities for efficient and secure financial transactions 
    between bank accounts, mobile wallets, and cryptocurrency wallets. Built for integration with banking systems 
    and financial platforms, it ensures high performance, reliability, and security for financial operations.

    Features:
    ---------
    - **Cryptocurrency Transactions**: 
      Perform transactions with leading cryptocurrencies, such as USDT, BTC, ETH, and others.
    - **Cross-Border Fund Transfers**: 
      Transfer funds directly to bank accounts and mobile wallets worldwide.
    - **Banking System Integration**: 
      Easily integrate with banking systems and mobile wallet platforms.
    - **Secure and Scalable**: 
      Designed with high-security standards and scalability to support enterprise needs.
    - **Comprehensive Documentation**: 
      Detailed request and response formats for smooth integration with financial systems.

    Transaction Details:
    --------------------
    - **Currency**: All transaction amounts must be specified in United States Dollars (USD). For example: `99000`.
    - **Limits**:
      - Minimum transaction amount: $100
      - Maximum transaction amount: $200,000,000

    Authentication:
    ---------------
    Access to the API is secured through an API key. Include the API key in the header of each request to authenticate.

    Example:
    --------
    ```bash
    curl -H "Authorization: your-API-KEY" http://BASE_URL/api/transactions
    ```

    This API provides a powerful interface for financial institutions, cryptocurrency platforms, and mobile wallet 
    providers to streamline their financial operations globally. For more details on endpoints, request parameters, 
    and response formats, refer to the full API documentation.
    """,
    docs=Redoc(),
    auth=ApiKey()
)

@api.get("/bank-servers", response=List[BankServerSchema])
def list_bank_servers(request):
    """
    List all bank servers.

    Retrieve a list of all bank servers registered in the system.

    Returns:
        List[BankServerSchema]: List of bank server details.

    Example Response:
    ```json
    [
        {
            "id": 1,
            "name": "Main Bank Server",
            "server_ip_address": "192.168.1.100"
        },
        {
            "id": 2,
            "name": "Backup Bank Server",
            "server_ip_address": "192.168.1.101"
        }
    ]
    ```
    """
    bank_servers = BankServer.objects.all()
    return bank_servers

@api.get("/bank-servers/{server_id}", response=BankServerSchema)
def get_bank_server(request, server_id: int):
    """
    Retrieve a bank server.

    Get details of a bank server by its unique identifier.

    Args:
        server_id (int): ID of the bank server to retrieve.

    Returns:
        BankServerSchema: Details of the requested bank server.

    Example Request:
    ```
    GET /bank-servers/1
    ```

    Example Response:
    ```json
    {
        "id": 1,
        "name": "Main Bank Server",
        "server_ip_address": "192.168.1.100"
    }
    ```
    """
    bank_server = get_object_or_404(BankServer, id=server_id)
    return bank_server

@api.post("/bank-servers", response=BankServerSchema)
def create_bank_server(request, payload: BankServerSchema):
    """
    Create a new bank server.

    Add a new bank server to the system with the provided details.

    Args:
        payload (BankServerSchema): Details of the new bank server.

    Returns:
        BankServerSchema: Details of the created bank server.

    Example Request:
    ```json
    {
        "name": "New Bank Server",
        "server_ip_address": "192.168.1.102"
    }
    ```

    Example Response:
    ```json
    {
        "id": 3,
        "name": "New Bank Server",
        "server_ip_address": "192.168.1.102"
    }
    ```
    """
    bank_server = BankServer.objects.create(
        name=payload.name,
        server_ip_address=payload.server_ip_address,
    )
    return bank_server

@api.put("/bank-servers/{server_id}", response=BankServerSchema)
def update_bank_server(request, server_id: int, payload: BankServerSchema):
    """
    Update a bank server.

    Modify the details of an existing bank server by its unique identifier.

    Args:
        server_id (int): ID of the bank server to update.
        payload (BankServerSchema): New details for the bank server.

    Returns:
        BankServerSchema: Updated details of the bank server.

    Example Request:
    ```json
    {
        "name": "Updated Bank Server",
        "server_ip_address": "192.168.1.103"
    }
    ```

    Example Response:
    ```json
    {
        "id": 3,
        "name": "Updated Bank Server",
        "server_ip_address": "192.168.1.103"
    }
    ```
    """
    bank_server = get_object_or_404(BankServer, id=server_id)
    bank_server.name = payload.name
    bank_server.server_ip_address = payload.server_ip_address
    bank_server.save()
    return bank_server

@api.delete("/bank-servers/{server_id}", response={204: None})
def delete_bank_server(request, server_id: int):
    """
    Delete a bank server.

    Remove a bank server from the system by its unique identifier.

    Args:
        server_id (int): ID of the bank server to delete.

    Returns:
        204: Successful deletion.
    """
    bank_server = get_object_or_404(BankServer, id=server_id)
    bank_server.delete()
    return 204, None

@api.get("/bank-accounts", response=List[BankAccountSchema])
def list_bank_accounts(request):
    """
    Get a list of all bank accounts.

    Retrieve a list of all bank accounts registered in the system.

    Returns:
        List[BankAccountSchema]: List of bank account details.

    Example Response:
    ```json
    [
        {
            "id": 1,
            "bank_server": {
                "id": 1,
                "name": "Main Bank Server",
                "server_ip_address": "192.168.1.100"
            },
            "account_name": "Checking Account",
            "account_number": "123456789"
        },
        {
            "id": 2,
            "bank_server": {
                "id": 2,
                "name": "Backup Bank Server",
                "server_ip_address": "192.168.1.101"
            },
            "account_name": "Savings Account",
            "account_number": "987654321"
        }
    ]
    ```
    """
    bank_accounts = BankAccount.objects.select_related('bank_server').all()
    return bank_accounts

@api.get("/bank-accounts/{account_id}", response=BankAccountSchema)
def get_bank_account(request, account_id: int):
    """
    Get a bank account.

    Retrieve the details of a bank account by its unique identifier.

    Args:
        account_id (int): ID of the bank account to retrieve.

    Returns:
        BankAccountSchema: Details of the requested bank account.

    Example Request:
    ```
    GET /bank-accounts/1
    ```

    Example Response:
    ```json
    {
        "id": 1,
        "bank_server": {
            "id": 1,
            "name": "Main Bank Server",
            "server_ip_address": "192.168.1.100"
        },
        "account_name": "Checking Account",
        "account_number": "123456789"
    }
    ```
    """
    bank_account = get_object_or_404(BankAccount.objects.select_related('bank_server'), id=account_id)
    return bank_account

@api.post("/bank-accounts", response=BankAccountSchema)
def create_bank_account(request, payload: BankAccountCreateSchema):
    """
    Create a new bank account.

    Add a new bank account to the system with the provided details.

    Args:
        payload (BankAccountCreateSchema): Details of the new bank account.

    Returns:
        BankAccountSchema: Details of the created bank account.

    Example Request:
    ```json
    {
        "bank_server": 1,
        "account_name": "Payroll Account",
        "account_number": "987654321"
    }
    ```

    Example Response:
    ```json
    {
        "id": 3,
        "bank_server": {
            "id": 1,
            "name": "Main Bank Server",
            "server_ip_address": "192.168.1.100"
        },
        "account_name": "Payroll Account",
        "account_number": "987654321"
    }
    ```
    """
    bank_server = get_object_or_404(BankServer, id=payload.bank_server)
    bank_account = BankAccount.objects.create(
        bank_server=bank_server,
        account_name=payload.account_name,
        account_number=payload.account_number,
    )
    return bank_account

@api.put("/bank-accounts/{account_id}", response=BankAccountSchema)
def update_bank_account(request, account_id: int, payload: BankAccountCreateSchema):
    """
    Update a bank account.

    Modify the details of a bank account by its unique identifier.

    Args:
        account_id (int): ID of the bank account to update.
        payload (BankAccountCreateSchema): New details for the bank account.

    Returns:
        BankAccountSchema: Updated details of the bank account.

    Example Request:
    ```json
    {
        "bank_server": 2,
        "account_name": "Updated Savings Account",
        "account_number": "654321987"
    }
    ```

    Example Response:
    ```json
    {
        "id": 2,
        "bank_server": {
            "id": 2,
            "name": "Backup Bank Server",
            "server_ip_address": "192.168.1.101"
        },
        "account_name": "Updated Savings Account",
        "account_number": "654321987"
    }
    ```
    """
    bank_account = get_object_or_404(BankAccount, id=account_id)
    bank_server = get_object_or_404(BankServer, id=payload.bank_server)
    bank_account.bank_server = bank_server
    bank_account.account_name = payload.account_name
    bank_account.account_number = payload.account_number
    bank_account.save()
    return bank_account

@api.delete("/bank-accounts/{account_id}", response={204: None})
def delete_bank_account(request, account_id: int):
    """
    Delete a bank account.

    Remove a bank account from the system by its unique identifier.

    Args:
        account_id (int): ID of the bank account to delete.

    Returns:
        204: Successful deletion.
    """
    bank_account = get_object_or_404(BankAccount, id=account_id)
    bank_account.delete()
    return 204, None

@api.get("/transactions", response=List[TransactionSchema])
def list_transactions(request):
    """
    List all transactions.

    Retrieve a list of all transactions that have occurred.

    Returns:
        List[TransactionSchema]: List of transaction details.

    Example Response:
    ```json
    [
        {
            "id": 1,
            "transaction_type": "bank_transfer",
            "amount": 1000.00,
            "source_account": {
                "id": 1,
                "bank_server": {
                    "id": 1,
                    "name": "Main Bank Server",
                    "server_ip_address": "192.168.1.100"
                },
                "account_name": "Checking Account",
                "account_number": "123456789"
            },
            "target_iban": "DE1234567890",
            "target_swift_code": "BANKDEFF",
            "target_bank_account_number": "987654321",
            "target_bank_name": "Foreign Bank",
            "target_country": "Germany",
            "provider": "TransferWise",
            "status": "pending"
        },
        {
            "id": 2,
            "transaction_type": "mobile_transfer",
            "amount": 50.00,
            "source_account": {
                "id": 2,
                "bank_server": {
                    "id": 2,
                    "name": "Backup Bank Server",
                    "server_ip_address": "192.168.1.101"
                },
                "account_name": "Savings Account",
                "account_number": "987654321"
            },
            "target_phone_number": "+1 555-1234",
            "provider": "CashApp",
            "status": "completed"
        }
    ]
    ```
    """
    transactions = Transaction.objects.select_related('source_account').all()
    return [TransactionSchema.from_transaction(t) for t in transactions]

@api.get("/transactions/{transaction_id}", response=TransactionSchema)
def get_transaction(request, transaction_id: int):
    """
    Retrieve a transaction.

    Get details of a transaction by its unique identifier.

    Args:
        transaction_id (int): ID of the transaction to retrieve.

    Returns:
        TransactionSchema: Details of the requested transaction.

    Example Request:
    ```
    GET /transactions/1
    ```

    Example Response:
    ```json
    {
        "id": 1,
        "transaction_type": "bank_transfer",
        "amount": 1000.00,
        "source_account": {
            "id": 1,
            "bank_server": {
                "id": 1,
                "name": "Main Bank Server",
                "server_ip_address": "192.168.1.100"
            },
            "account_name": "Checking Account",
            "account_number": "123456789"
        },
        "target_iban": "DE1234567890",
        "target_swift_code": "BANKDEFF",
        "target_bank_account_number": "987654321",
        "target_bank_name": "Foreign Bank",
        "target_country": "Germany",
        "provider": "TransferWise",
        "status": "pending"
    }
    ```
    """
    transaction = get_object_or_404(Transaction.objects.select_related('source_account'), id=transaction_id)
    return TransactionSchema.from_transaction(transaction)

@api.post("/transactions", response=TransactionSchema)
def create_transaction(request, payload: TransactionCreateSchema):
    """
    Create a new transaction.

    Add a new transaction to the system, either a bank transfer or mobile money transfer. This API
    endpoint is used to transfer money from the bank server to the selected bank account globally.

    Args:
        payload (TransactionCreateSchema): Details of the new transaction.

    Returns:
        TransactionSchema: Details of the created transaction.

    Example Request (Bank Transfer):
    ```json
    {
        "transaction_type": "bank_transfer",
        "amount": 500.00,
        "source_account": 1,
        "target_iban": "GB0011223344",
        "target_swift_code": "BANKGB22",
        "target_bank_account_number": "55667788",
        "target_bank_name": "UK Bank",
        "target_country": "United Kingdom",
        "provider": "SWIFT"
    }
    ```

    Example Response (Bank Transfer):
    ```json
    {
        "id": 3,
        "transaction_type": "bank_transfer",
        "amount": 500.00,
        "source_account": {
            "id": 1,
            "bank_server": {
                "id": 1,
                "name": "Main Bank Server",
                "server_ip_address": "192.168.1.100"
            },
            "account_name": "Checking Account",
            "account_number": "123456789"
        },
        "target_iban": "GB0011223344",
        "target_swift_code": "BANKGB22",
        "target_bank_account_number": "55667788",
        "target_bank_name": "UK Bank",
        "target_country": "United Kingdom",
        "provider": "SWIFT",
        "status": "pending"
    }
    ```

    Example Request (Mobile Transfer):
    ```json
    {
        "transaction_type": "mobile_transfer",
        "amount": 50.00,
        "source_account": 2,
        "target_phone_number": "+1 555-1234",
        "provider": "CashApp"
    }
    ```

    Example Response (Mobile Transfer):
    ```json
    {
        "id": 4,
        "transaction_type": "mobile_transfer",
        "amount": 50.00,
        "source_account": {
            "id": 2,
            "bank_server": {
                "id": 2,
                "name": "Backup Bank Server",
                "server_ip_address": "192.168.1.101"
            },
            "account_name": "Savings Account",
            "account_number": "987654321"
        },
        "target_phone_number": "+1 555-1234",
        "provider": "CashApp",
        "status": "pending"
    }
    ```
    """
    source_account = get_object_or_404(BankAccount, id=payload.source_account)

    transaction = Transaction.objects.create(
        transaction_type=payload.transaction_type,
        amount=payload.amount,
        source_account=source_account,
        target_iban=payload.target_iban,
        target_swift_code=payload.target_swift_code,
        target_bank_account_number=payload.target_bank_account_number,
        target_bank_name=payload.target_bank_name,
        target_phone_number=payload.target_phone_number,
        target_country=payload.target_country,
        provider=payload.provider,
        status="pending",
    )
    return TransactionSchema.from_transaction(transaction)

@api.put("/transactions/{transaction_id}/status", response=TransactionSchema)
def update_transaction_status(request, transaction_id: int, payload: TransactionStatusUpdateSchema):
    """
    Update the status of a transaction.

    Modify the status of an existing transaction by its unique identifier.

    Args:
        transaction_id (int): ID of the transaction to update.
        payload (TransactionStatusUpdateSchema): New status for the transaction.

    Returns:
        TransactionSchema: Updated details of the transaction.

    Example Request:
    ```json
    {
        "status": "completed"
    }
    ```

    Example Response:
    ```json
    {
        "id": 3,
        "transaction_type": "bank_transfer",
        "amount": 500.00,
        "source_account": {
            "id": 1,
            "bank_server": {
                "id": 1,
                "name": "Main Bank Server",
                "server_ip_address": "192.168.1.100"
            },
            "account_name": "Checking Account",
            "account_number": "123456789"
        },
        "target_iban": "GB0011223344",
        "target_swift_code": "BANKGB22",
        "target_bank_account_number": "55667788",
        "target_bank_name": "UK Bank",
        "target_country": "United Kingdom",
        "provider": "SWIFT",
        "status": "completed"
    }
    ```
    """
    transaction = get_object_or_404(Transaction, id=transaction_id)
    transaction.status = payload.status
    transaction.save()
    return TransactionSchema.from_transaction(transaction)

@api.delete("/transactions/{transaction_id}", response={204: None})
def delete_transaction(request, transaction_id: int):
    """
    Delete a transaction.

    Remove a transaction from the system by its unique identifier.

    Args:
        transaction_id (int): ID of the transaction to delete.

    Returns:
        204: Successful deletion.
    """
    transaction = get_object_or_404(Transaction, id=transaction_id)
    transaction.delete()
    return 204, None