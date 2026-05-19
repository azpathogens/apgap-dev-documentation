"""
GCP Workflows client for executing and monitoring workflow executions.

Uses the official google-cloud-workflows Python client library.
https://cloud.google.com/python/docs/reference/workflows/latest
"""


class WorkflowsClient:
    """
    Client for interacting with Google Cloud Workflows Executions API.

    Provides methods to execute workflows and poll their status

    Uses the official google-cloud-workflows Python client library.
    """

    def __init__(self):
        """Initialize the Workflows Executions client."""

    def execute_workflow(
        self,
        workflow_id: str,
        project_id: str,
        location: str,
        arguments: dict | None = None,
    ) -> Execution | None:
        """
        Execute a workflow with the given arguments.

        Args:
            workflow_id: The ID of the workflow to execute
            project_id: The GCP project ID where the workflow resides
            location: The location of the workflow (e.g., 'us-central1')
            arguments: Dictionary of arguments to pass to the workflow

        Returns:
            Execution: The execution object containing the execution name and state,
                       or None if execution failed
        """

    def get_execution_status(self, execution_name: str) -> Execution | None:
        """
        Get the current status of a workflow execution.

        Args:
            execution_name: The full resource name of the execution
                           (e.g., projects/PROJECT/locations/LOCATION/workflows/WORKFLOW/executions/EXECUTION_ID)

        Returns:
            Execution: The execution object with current state, or None if retrieval failed
        """

    def is_execution_complete(self, state: Execution.State | int) -> bool:
        """
        Check if the execution state indicates the workflow is complete.

        Args:
            state: The execution state from the Workflows API (can be enum or int)

        Returns:
            bool: True if the workflow execution is complete, False otherwise
        """

    def is_execution_successful(self, state: Execution.State | int) -> bool:
        """
        Check if the execution state indicates the workflow succeeded.

        Args:
            state: The execution state from the Workflows API (can be enum or int)

        Returns:
            bool: True if the workflow execution was successful, False otherwise
        """
    @staticmethod
    def get_state_name(state: Execution.State | int) -> str:
        """
        Get a human-readable name for the execution state.

        Args:
            state: The execution state from the Workflows API

        Returns:
            str: Human-readable state name
        """
