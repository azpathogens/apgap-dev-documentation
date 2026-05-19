"""Values passed as Cloud Build substitutions for lab Terraform pipelines."""


def lab_billing_account_substitution(lab: Lab) -> str:
    """
    Billing account ID for Terraform ``-var billing_account_id=``.

    Order: lab-specific field, then Django ``LAB_BILLING_ACCOUNT_ID`` (from env / IaC).
    Empty string means Terraform uses the lab module default (constants billing_id).
    """
