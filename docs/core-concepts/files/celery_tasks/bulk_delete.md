
def _collect_batch_recipients(lab, files, actor) -> set:
    """
    Resolve the union of notification recipients for a bulk batch.

    - lab directors for `lab` (no-op if lab is None)
    - all platform admins
    - uploaders of the files in the batch (from already-loaded rows)
    - the initiating actor (so they always see their own batch)
    """


def _build_success_details(
    actor,
    succeeded: list[dict],
    lab_name: str,
) -> str:
    # bulk delete refuses dataset-entangled files at the view layer, so we
    # don't have to speak to impacted datasets here (unlike single delete).
    # were also constrained to a single lab, so the lab is named once
    # at the top rather than per-file


def _dispatch_aggregated_notification(
    actor,
    succeeded: list[dict],
    recipients: set,
    failures: list[dict],
    lab_name: str,
) -> None:

    # separate notification to the initiator summarizing any failures. kept out
    # of the shared notification so other recipients don't see internal error
    # messages like raw GCS exceptions


@shared_task(bind=True)
def bulk_hard_delete_files(
    self,
    *,
    file_ids: list[int],
    deleted_by_id: int,
    batch_id: str,
    justification: str = "",
) -> dict:
    """
    Hard-delete a batch of files and send one aggregated notification.

    re-checks per-file invariants (see check_bulk_deletable)

    Args:
        file_ids: IDs that passed pre-validation
        deleted_by_id: user who initiated the deletion
        batch_id: shared UUID written to each Deletion.additional_data for audit purposes
        justification: optional. Forwarded to each per-file `hard_delete`,
            which falls back to a status-derived reason when this is empty.

    Returns:
        {"batch_id", "succeeded_ids", "failures"}
    """

    # pre-fetch every file in one query preserving request order by looking
    # up files through a dict keyed on id

    # re-check every per-file rule the view enforced, anything that fails
    # here is drift between enqueue and execution
