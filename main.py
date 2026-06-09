"""
OOP-SOLID-Principles-CRM — Customer Relationship Management
Demonstrates ALL 5 SOLID Principles with before/after examples
Author  : Kushagra Bansal — Project Lab India
Run     : python main.py
"""
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import List, Optional

# ════════════════════════════════════════════════════════════
# S — Single Responsibility Principle
# "A class should have only one reason to change"
# ════════════════════════════════════════════════════════════

class Customer:
    """ONLY responsible for customer data — nothing else"""
    def __init__(self, id, name, email, phone, company=""):
        self.id       = id
        self.name     = name
        self.email    = email
        self.phone    = phone
        self.company  = company
        self.created  = datetime.now()

    def __str__(self):
        return f"Customer[{self.id}] {self.name} | {self.email} | {self.company}"

class CustomerValidator:
    """ONLY responsible for validation"""
    @staticmethod
    def validate_email(email):
        import re
        if not re.match(r'^[\w.-]+@[\w.-]+\.\w+$', email):
            raise ValueError(f"Invalid email: {email}")

    @staticmethod
    def validate_phone(phone):
        if not (phone.isdigit() and len(phone) == 10):
            raise ValueError(f"Phone must be 10 digits: {phone}")

    @staticmethod
    def validate_customer(customer):
        CustomerValidator.validate_email(customer.email)
        CustomerValidator.validate_phone(customer.phone)
        return True

class CustomerEmailService:
    """ONLY responsible for sending emails"""
    def send_welcome_email(self, customer):
        print(f"  📧 Welcome email → {customer.email}")

    def send_followup_email(self, customer, message):
        print(f"  📧 Follow-up → {customer.email}: {message}")

class CustomerReportGenerator:
    """ONLY responsible for generating reports"""
    def generate_summary(self, customers):
        print(f"\n  📊 Customer Summary: {len(customers)} customers")
        for c in customers:
            print(f"     {c}")


# ════════════════════════════════════════════════════════════
# O — Open/Closed Principle
# "Open for extension, closed for modification"
# ════════════════════════════════════════════════════════════

class DiscountStrategy(ABC):
    """Base — open for extension, not modification"""
    @abstractmethod
    def calculate(self, amount: float, customer: Customer) -> float:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass

class NoDiscount(DiscountStrategy):
    def calculate(self, amount, customer): return 0.0
    def get_description(self): return "No Discount"

class PercentageDiscount(DiscountStrategy):
    def __init__(self, pct): self.pct = pct
    def calculate(self, amount, customer): return amount * self.pct
    def get_description(self): return f"{self.pct*100:.0f}% Flat Discount"

class LoyaltyDiscount(DiscountStrategy):
    """New discount type — EXTEND without modifying existing code"""
    def __init__(self, loyalty_years_threshold=2):
        self.threshold = loyalty_years_threshold

    def calculate(self, amount, customer):
        years = (datetime.now() - customer.created).days / 365
        if years >= self.threshold:
            return amount * 0.15
        return amount * 0.05

    def get_description(self): return f"Loyalty Discount (>{self.threshold}yr = 15%)"

class SeasonalDiscount(DiscountStrategy):
    """Another extension — no modification to existing classes"""
    SEASONAL_RATES = {12: 0.20, 1: 0.20, 11: 0.15, 10: 0.10}

    def calculate(self, amount, customer):
        month = datetime.now().month
        rate = self.SEASONAL_RATES.get(month, 0.0)
        return amount * rate

    def get_description(self):
        return f"Seasonal Discount ({datetime.now().strftime('%B')})"


# ════════════════════════════════════════════════════════════
# L — Liskov Substitution Principle
# "Subclass objects must be substitutable for parent objects"
# ════════════════════════════════════════════════════════════

class Notification(ABC):
    """Contract: all notifications can be sent"""
    @abstractmethod
    def send(self, recipient: str, message: str) -> bool:
        pass

    @abstractmethod
    def get_channel(self) -> str:
        pass

class EmailNotification(Notification):
    def send(self, recipient, message):
        print(f"  📧 EMAIL → {recipient}: {message}")
        return True

    def get_channel(self): return "Email"

class SMSNotification(Notification):
    def send(self, recipient, message):
        print(f"  📱 SMS → {recipient}: {message[:160]}")  # SMS limit
        return True

    def get_channel(self): return "SMS"

class WhatsAppNotification(Notification):
    def send(self, recipient, message):
        print(f"  💬 WHATSAPP → {recipient}: {message}")
        return True

    def get_channel(self): return "WhatsApp"

class PushNotification(Notification):
    def send(self, recipient, message):
        print(f"  🔔 PUSH → {recipient}: {message[:50]}...")
        return True

    def get_channel(self): return "Push"

def send_campaign(notifications: List[Notification], customers: List[Customer], msg: str):
    """LSP: works with ANY Notification subclass without knowing the type"""
    results = []
    for notification in notifications:
        for customer in customers:
            ok = notification.send(customer.email, msg)
            results.append((notification.get_channel(), customer.name, ok))
    return results


# ════════════════════════════════════════════════════════════
# I — Interface Segregation Principle
# "Clients should not be forced to depend on interfaces they don't use"
# ════════════════════════════════════════════════════════════

class Readable(ABC):
    @abstractmethod
    def get(self, id): pass

    @abstractmethod
    def list_all(self): pass

class Writable(ABC):
    @abstractmethod
    def save(self, entity): pass

    @abstractmethod
    def delete(self, id): pass

class Searchable(ABC):
    @abstractmethod
    def search(self, query: str): pass

class Exportable(ABC):
    @abstractmethod
    def export_to_csv(self, filepath: str): pass

# Each repository implements ONLY what it needs
class CustomerRepository(Readable, Writable, Searchable):
    """Read + Write + Search — no export needed"""
    def __init__(self):
        self._store = {}

    def save(self, customer: Customer):
        self._store[customer.id] = customer
        print(f"  💾 Saved: {customer}")

    def get(self, id):
        return self._store.get(id)

    def list_all(self):
        return list(self._store.values())

    def delete(self, id):
        if id in self._store:
            del self._store[id]

    def search(self, query):
        q = query.lower()
        return [c for c in self._store.values()
                if q in c.name.lower() or q in c.email.lower() or q in c.company.lower()]

class ReportRepository(Readable, Exportable):
    """Read + Export only — no write permission"""
    def __init__(self, customer_repo):
        self._repo = customer_repo

    def get(self, id):
        return self._repo.get(id)

    def list_all(self):
        return self._repo.list_all()

    def export_to_csv(self, filepath):
        customers = self.list_all()
        import csv, io
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["ID","Name","Email","Phone","Company"])
        for c in customers:
            writer.writerow([c.id, c.name, c.email, c.phone, c.company])
        print(f"  📄 Exported {len(customers)} customers to {filepath}")
        return output.getvalue()


# ════════════════════════════════════════════════════════════
# D — Dependency Inversion Principle
# "Depend on abstractions, not concretions"
# ════════════════════════════════════════════════════════════

class ICustomerRepository(ABC):
    """Abstraction — high-level modules depend on this"""
    @abstractmethod
    def save(self, customer): pass
    @abstractmethod
    def get(self, id): pass
    @abstractmethod
    def list_all(self): pass

class INotificationService(ABC):
    """Abstraction for notification"""
    @abstractmethod
    def notify(self, customer, message): pass

class InMemoryCustomerRepository(ICustomerRepository):
    """Concrete implementation — swappable"""
    def __init__(self): self._data = {}
    def save(self, c): self._data[c.id] = c
    def get(self, id): return self._data.get(id)
    def list_all(self): return list(self._data.values())

class EmailNotificationService(INotificationService):
    """Concrete notification — swappable"""
    def notify(self, customer, message):
        print(f"  📧 Notifying {customer.name}: {message}")

class CRMService:
    """HIGH-LEVEL module — depends on ABSTRACTIONS, not concretions
    Dependencies injected via constructor (Dependency Injection)
    """
    def __init__(self,
                 repo: ICustomerRepository,
                 notifier: INotificationService,
                 discount: DiscountStrategy):
        self._repo      = repo       # Injected — any ICustomerRepository works
        self._notifier  = notifier   # Injected — any INotificationService works
        self._discount  = discount   # Injected — any DiscountStrategy works

    def onboard_customer(self, customer: Customer):
        """Orchestrates onboarding using injected dependencies"""
        CustomerValidator.validate_customer(customer)
        self._repo.save(customer)
        self._notifier.notify(customer, f"Welcome to Project Lab India CRM, {customer.name}!")
        print(f"  ✅ Customer onboarded: {customer}")

    def calculate_invoice(self, customer: Customer, amount: float) -> float:
        discount_amt = self._discount.calculate(amount, customer)
        final        = amount - discount_amt
        print(f"  💰 Invoice: ₹{amount:,.2f} - {self._discount.get_description()} "
              f"₹{discount_amt:,.2f} = ₹{final:,.2f}")
        return final

    def get_all_customers(self):
        return self._repo.list_all()

    def search_customers(self, query):
        all_c = self._repo.list_all()
        q = query.lower()
        return [c for c in all_c if q in c.name.lower() or q in c.email.lower()]


if __name__ == "__main__":
    print("═"*65)
    print("  OOP SOLID Principles — CRM System")
    print("  Project Lab India")
    print("═"*65)

    # ── Dependency Injection — swap implementations easily
    crm_v1 = CRMService(
        repo      = InMemoryCustomerRepository(),
        notifier  = EmailNotificationService(),
        discount  = LoyaltyDiscount(years=1)
    )

    crm_v2 = CRMService(
        repo      = InMemoryCustomerRepository(),
        notifier  = EmailNotificationService(),
        discount  = SeasonalDiscount()
    )

    # Create customers
    c1 = Customer("C001", "Kushagra Bansal",  "kushagra@pli.in",  "9876543210", "Project Lab India")
    c2 = Customer("C002", "Priya Sharma",     "priya@startup.in", "9876543211", "TechStartup Ltd")
    c3 = Customer("C003", "Rahul Agarwal",    "rahul@company.in", "9876543212", "Agarwal Corp")

    print("\n── S: Single Responsibility ──")
    validator = CustomerValidator()
    email_svc = CustomerEmailService()
    reporter  = CustomerReportGenerator()

    for c in [c1, c2, c3]:
        validator.validate_customer(c)
        crm_v1.onboard_customer(c)
        email_svc.send_welcome_email(c)

    print("\n── O: Open/Closed — Discount Strategies ──")
    for strategy in [NoDiscount(), PercentageDiscount(0.10), LoyaltyDiscount(), SeasonalDiscount()]:
        crm = CRMService(InMemoryCustomerRepository(), EmailNotificationService(), strategy)
        crm.onboard_customer(Customer("C999","Test","test@t.com","1234567890"))
        crm.calculate_invoice(c1, 50000.0)

    print("\n── L: Liskov Substitution — Notifications ──")
    channels = [EmailNotification(), SMSNotification(), WhatsAppNotification(), PushNotification()]
    send_campaign(channels, [c1, c2], "Exclusive offer this season!")

    print("\n── I: Interface Segregation ──")
    cust_repo   = CustomerRepository()
    for c in [c1, c2, c3]: cust_repo.save(c)
    report_repo = ReportRepository(cust_repo)
    results = cust_repo.search("pli")
    print(f"  Search 'pli': {[c.name for c in results]}")
    report_repo.export_to_csv("customers.csv")

    print("\n── D: Dependency Inversion ──")
    print("  Same CRMService works with ANY injected repository or notifier!")
    print("  crm_v1 uses LoyaltyDiscount, crm_v2 uses SeasonalDiscount")
    crm_v1.calculate_invoice(c1, 100000)
    crm_v2.calculate_invoice(c1, 100000)

    reporter.generate_summary(crm_v1.get_all_customers())
