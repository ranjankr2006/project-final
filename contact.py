import os
import re
import logging
from cryptography.fernet import Fernet
from datetime import datetime

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("BankDetailsLogger")

# --- Encryption Setup ---
class EncryptionService:
    def __init__(self, key: str):
        self.fernet = Fernet(key.encode())

    def encrypt(self, value: str) -> str:
        return self.fernet.encrypt(value.encode()).decode()

    def decrypt(self, value: str) -> str:
        return self.fernet.decrypt(value.encode()).decode()

# --- Validators ---
class BankValidator:
    @staticmethod
    def validate_account_number(account_number: str) -> bool:
        return bool(re.fullmatch(r"\d{9,18}", account_number))

    @staticmethod
    def validate_routing_number(routing_number: str) -> bool:
        return bool(re.fullmatch(r"\d{9}", routing_number))

    @staticmethod
    def validate_holder_name(name: str) -> bool:
        return bool(re.fullmatch(r"[A-Za-z\s]{2,50}", name))

# --- Bank Details Class ---
class BankDetails:
    def __init__(self, encryption_service: EncryptionService, account_number: str, routing_number: str, holder_name: str):
        if not BankValidator.validate_account_number(account_number):
            raise ValueError("Invalid account number format.")
        if not BankValidator.validate_routing_number(routing_number):
            raise ValueError("Invalid routing number format.")
        if not BankValidator.validate_holder_name(holder_name):
            raise ValueError("Invalid holder name format.")

        self.encryption_service = encryption_service
        self._encrypted_account_number = encryption_service.encrypt(account_number)
        self._encrypted_routing_number = encryption_service.encrypt(routing_number)
        self._holder_name = holder_name
        logger.info("Bank details initialized for holder: %s", holder_name)

    def get_decrypted_info(self) -> dict:
        return {
            "holder_name": self._holder_name,
            "account_number": self.encryption_service.decrypt(self._encrypted_account_number),
            "routing_number": self.encryption_service.decrypt(self._encrypted_routing_number)
        }

    def __str__(self):
        return f"BankDetails(holder={self._holder_name})"

# --- Bank Account Simulation ---
class BankAccount:
    def __init__(self, bank_details: BankDetails):
        self.bank_details = bank_details
        self.balance = 0.0
        self.transactions = []

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self.transactions.append((datetime.now(), f"Deposited ${amount:.2f}"))
        logger.info("Deposited $%.2f to %s", amount, self.bank_details._holder_name)

    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount
        self.transactions.append((datetime.now(), f"Withdrew ${amount:.2f}"))
        logger.info("Withdrew $%.2f from %s", amount, self.bank_details._holder_name)

    def get_statement(self):
        statement = {
            "account_holder": self.bank_details._holder_name,
            "balance": self.balance,
            "transactions": self.transactions
        }
        return statement

    def print_statement(self):
        info = self.get_statement()
        print(f"\nStatement for {info['account_holder']}:")
        print(f"Balance: ${info['balance']:.2f}")
        print("Transactions:")
        for time, desc in info['transactions']:
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {desc}")
        print()

# --- Key Generation (Temporary) ---
def generate_encryption_key() -> str:
    return Fernet.generate_key().decode()

# --- Main Execution (Example Simulation) ---
if __name__ == "__main__":
    # In real use, this would come from a secrets manager or environment variable
    encryption_key = generate_encryption_key()
    os.environ["BANK_ENCRYPTION_KEY"] = encryption_key

    key = os.getenv("BANK_ENCRYPTION_KEY")
    encryption_service = EncryptionService(key)

    # Create fake bank details
    try:
        details = BankDetails(
            encryption_service=encryption_service,
            account_number="123456789123",
            routing_number="987654321",
            holder_name="Alice Smith"
        )
        account = BankAccount(details)
        account.deposit(500.00)
        account.withdraw(120.00)
        account.deposit(250.00)
        account.print_statement()

        decrypted = details.get_decrypted_info()
        print("Decrypted Bank Details:")
        for k, v in decrypted.items():
            print(f"{k}: {v}")

    except ValueError as ve:
        logger.error("Validation error: %s", ve)

