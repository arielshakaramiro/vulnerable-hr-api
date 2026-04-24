# config.py — Application configuration
import os

# ============================================================
# DATABASE CONFIG
# ============================================================
DB_HOST     = "prod-db.internal.company.com"
DB_PORT     = 5432
DB_NAME     = "hr_production"
DB_USER     = "admin"
DB_PASSWORD = "Adm1n@2024!Super"        # VULN: hardcoded credential

# ============================================================
# THIRD-PARTY API KEYS
# ============================================================
SENDGRID_API_KEY  = "SG.xK9mN2pQrT5vW8yZ.aB3cD6eF9gH1iJ4kL7mN0oP2qR5sT8uV1wX4yZ7"
OPENAI_API_KEY    = "sk-proj-xK9mN2pQrT5vW8yZaB3cD6eF9gH1iJ4kL7mN0oP"
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
JWT_SECRET        = "mysecret123"        # VULN: weak JWT secret

# ============================================================
# AWS CREDENTIALS
# ============================================================
AWS_ACCESS_KEY_ID     = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
AWS_REGION            = "ap-southeast-1"

# ============================================================
# APP CONFIG
# ============================================================
DEBUG         = True                     # VULN: debug mode in production
SECRET_KEY    = "dev-secret-key-change-in-prod"
ALLOWED_HOSTS = ["*"]                    # VULN: wildcard host
