# SOLID Principles

## S — Single Responsibility
One class, one reason to change.
Customer stores data. CustomerValidator validates. EmailService sends emails.

## O — Open/Closed
Open for extension, closed for modification.
Add new DiscountStrategy without touching existing code.

## L — Liskov Substitution
Subclass can replace parent without breaking behavior.
Any Notification subclass works wherever Notification is expected.

## I — Interface Segregation
Don't force clients to implement unused interfaces.
ReportRepository only needs Readable+Exportable, not Writable.

## D — Dependency Inversion
Depend on abstractions, not concretions.
CRMService takes ICustomerRepository, not InMemoryCustomerRepository.

## Interview Questions
1. Explain each SOLID principle with example.
2. Which principle is hardest to follow and why?
3. How does DI relate to DIP?
4. What problem does OCP solve in large codebases?
5. What is the relationship between LSP and polymorphism?
