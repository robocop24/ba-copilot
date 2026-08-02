def retrieve_similar_brd(requirement: str) -> str:
    """Retrieve relevant BRD knowledge for a given requirement."""

    brd_knowledge_base = {
        "login": """
Login System:
- Password Policy: minimum 12 characters, mixed case + digits + symbols
- MFA: TOTP-based two-factor authentication
- Session Timeout: 15 minutes of inactivity
- Password Reset: self-service via email verification link
- Account Lockout: 5 failed attempts → 30-minute lockout
""",
        "payment": """
Payment Gateway Integration:
- Supported methods: credit card, PayPal, bank transfer
- PCI-DSS Level 1 compliance required
- Idempotency keys for duplicate transaction prevention
- Refund window: 30 days
- Currency: USD, EUR, GBP (expandable)
""",
        "notification": """
Notification Service:
- Channels: email, SMS, push notification
- Email provider: SendGrid with fallback to SES
- Rate limiting: 100 notifications/minute per user
- Templates: localized (EN, ES, FR)
- Retry policy: exponential backoff, max 5 attempts
""",
        "customer portal": """
Customer Portal:
- Self-service account management
- Order history with 7-year retention
- Live chat with 30-second SLA
- Knowledge base with full-text search
- Role-based access: Customer, Manager, Admin
""",
    }

    key = requirement.strip().lower()
    for topic, content in brd_knowledge_base.items():
        if topic in key or key in topic:
            return content.strip()

    return (
        f"No specific BRD knowledge found for '{requirement}'.\n"
        "Available topics: login, payment, notification, customer portal"
    )

