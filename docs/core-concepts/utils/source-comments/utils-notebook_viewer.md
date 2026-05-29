"""
GCP IAM client for granting access to Vertex AI Workbench notebook instances.

Instead of setting IAM on notebook instances directly (which fails with
FAILED_PRECONDITION on Terraform-provisioned service-account-mode instances),
this client grants ``roles/iam.serviceAccountUser`` on the notebook's dedicated
service account.  Users who hold ``actAs`` on the SA can access the JupyterLab
proxy, which is the intended mechanism for multi-user service-account-mode
Workbench instances.

The dedicated SA is created in Terraform with minimal permissions (logging +
startup script bucket access only), so granting ``actAs`` has a small blast
radius.

https://cloud.google.com/iam/docs/service-account-permissions
https://cloud.google.com/vertex-ai/docs/workbench/instances/manage-access-jupyterlab
"""


# The IAM policy version to request and set.  Version 3 supports conditional
# bindings and is the version Google recommends in all setIamPolicy examples.

# Retry configuration for setIamPolicy calls that fail with transient errors
# (etag conflicts, rate limits, etc.).


class NotebookAccessClient:
    """
    Client for managing user access to Vertex AI Workbench notebooks.

    Grants/revokes ``roles/iam.serviceAccountUser`` on the notebook's dedicated
    service account so that project members and lab directors can access the
    JupyterLab proxy.  Uses the IAM API v1 for service-account-level IAM.
    """
    # ------------------------------------------------------------------
    # IAM helpers (service-account level)
    # ------------------------------------------------------------------

    def _sa_resource(self):
        """Shortcut to the service-accounts resource of the IAM discovery client."""

    def _sa_resource_name(self, gcp_project_id: str, sa_email: str) -> str:
        """Build the fully-qualified resource name for a service account."""

    def _get_sa_policy(self, resource_name: str) -> dict | None:
        """
        Get the IAM policy for a service account.

        Requests policy version 3 so that the response always includes the
        version field (required by setIamPolicy).

        Args:
            resource_name: Fully-qualified SA resource name
                (e.g. 'projects/my-project/serviceAccounts/sa@my-project.iam...').

        Returns:
            The IAM policy dict, or None on failure.
        """

    def _set_sa_policy(self, resource_name: str, policy: dict) -> dict | None:
        """
        Set the IAM policy for a service account with retry on transient errors.

        Ensures the policy always carries ``version: 3`` before sending.  Retries
        on conflict / rate-limit / precondition errors with exponential backoff.

        Args:
            resource_name: Fully-qualified SA resource name.
            policy: The updated IAM policy dict (must include etag).

        Returns:
            The updated policy dict, or None on failure.
        """
    # ------------------------------------------------------------------
    # Role-binding reconciliation
    # ------------------------------------------------------------------

    def _sync_role_binding(
        self,
        resource_name: str,
        policy: dict,
        role: str,
        desired_members: set[str],
        display_context: str = "",
    ) -> bool:
        """
        Reconcile IAM bindings for a specific role on the given policy.

        Only modifies the binding for the specified role; other bindings are
        left untouched.
        """
    # ------------------------------------------------------------------
    # Sync orchestration
    # ------------------------------------------------------------------

    def sync_access(self, project) -> bool:
        """
        Sync notebook access for a project.

        Determines the desired set of users from the Project model (project users
        and lab directors) and reconciles the configured role binding on the
        project's dedicated notebook service account.

        Args:
            project: A Project model instance.

        Returns:
            True if sync completed successfully, False otherwise.
        """
