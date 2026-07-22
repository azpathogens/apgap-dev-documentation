"""
Resource calculator for SRA Human Scrubber GCP Batch jobs.

Calculates optimal compute resources (CPU, memory, disk) based on input
file size and compression type. This allows the workflow to dynamically
provision the right-sized VM instead of using hardcoded values.

The SRA scrubber pipeline (scrub.sh) has the following disk-intensive steps:
1. Decompress input to temp dir (gunzip/bunzip2 -> input.fastq)
2. Convert FASTQ to FASTA (temp.fasta, ~50% of decompressed size).
   input.fastq is NOT deleted; it is reused in step 3.
3. Pipeline: `aligns_to temp.fasta | cut_spots_fastq.py input.fastq > output.fastq`
   At this moment THREE files coexist on the boot disk:
     - input.fastq  (1.0x decompressed, read by cut_spots_fastq.py)
     - temp.fasta   (0.5x decompressed, read by aligns_to)
     - output.fastq (~1.0x decompressed; the scrubber masks/removes spots so
                     the output is approximately the same size as input)
4. Re-compress output (gzip/bzip2), then delete the uncompressed copy.

Peak boot disk usage occurs in step 3:
    container_image + OS + 2.5 * decompressed
"""


# Container overhead: google/cloud-sdk base image (~3 GB) + human_filter.db (~10 GB)
# OS, GCS FUSE, and miscellaneous overhead
# Combined fixed overhead

# Peak boot-disk multiplier (relative to decompressed FASTQ size). During the
# `aligns_to | cut_spots_fastq.py > output.fastq` pipeline three files coexist:
#   input.fastq (1.0x) + temp.fasta (0.5x) + output.fastq (1.0x) = 2.5x.
# Previously this was hardcoded at 1.5x, which omitted the output FASTQ and led
# to "No space left on device" failures in cut_spots_fastq.py on large inputs.

# Safety margin multiplier (~44% headroom; was 1.2 / 20% but bumped to absorb
# additional growth observed in production batch jobs running out of space).

# Typical compression ratios (compressed → decompressed)

# Resource tier thresholds (based on decompressed file size in GB)

# Minimum boot disk size to ensure small files always have headroom

# Resource configurations per tier


@dataclass(frozen=True)
class BatchJobResources:
    """Computed resource requirements for a Batch job."""

    def to_workflow_args(self) -> dict:
        """
        Convert to a dict of workflow arguments.

        Returns:
            dict with keys matching the GCP Workflow parameter names.
        """


def _estimate_decompressed_size_gb(file_size_bytes: int, *, is_gz: bool, is_bz: bool) -> float:
    """
    Estimate the decompressed file size based on compression type.

    Args:
        file_size_bytes: Size of the compressed file in bytes.
        is_gz: Whether the file is gzip compressed.
        is_bz: Whether the file is bzip2 compressed.

    Returns:
        Estimated decompressed size in GB.
    """


def _calculate_disk_size_gb(decompressed_gb: float) -> int:
    """
    Calculate required boot disk size.

    The scrub.sh pipeline's peak disk moment is during the
    `aligns_to | cut_spots_fastq.py > output.fastq` step, where the original
    input.fastq, the FASTA conversion, and the scrubbed output FASTQ all
    coexist on the boot disk simultaneously (see module docstring for details).

    Peak usage = fixed_overhead + 2.5 * decompressed

    Args:
        decompressed_gb: Estimated decompressed file size in GB.

    Returns:
        Required disk size in GB (rounded up to nearest 10 GB).
    """


def calculate_scrubber_resources(
    file_size_bytes: int | None,
    *,
    is_gz: bool,
    is_bz: bool,
) -> BatchJobResources:
    """
    Calculate optimal GCP Batch job resources for the SRA Human Scrubber.

    Determines disk size, CPU, memory, and thread count based on the
    input file's compressed size and compression type.

    For small-to-medium files (decompressed < 60 GB):
        8 CPUs, 15 GB RAM, 8 threads

    For large files (decompressed >= 60 GB):
        16 CPUs, 32 GB RAM, 16 threads

    Disk is always sized to fit the container image, decompressed FASTQ,
    FASTA conversion, and a ~44% safety margin.

    Args:
        file_size_bytes: Size of the input file in bytes, or None if unknown.
        is_gz: Whether the file is gzip compressed.
        is_bz: Whether the file is bzip2 compressed.

    Returns:
        BatchJobResources with computed resource values.
    """
