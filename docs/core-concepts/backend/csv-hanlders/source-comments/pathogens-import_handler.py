"""
CSV import handler for the Pathogen registry.

Functions similarly to the metadata_requirements CSVImportHandler

Only upserts by name. Deletions should happen explicitly via the API or Django admin
"""
