
# Deployment

### Cloud Build

- Google Cloud Build pipelines handle application deployment
- The development environment is deployed to the `development` namespace in GKE
- The deployment process:
  1. Builds a container image
  2. Uses Helm to apply changes to Kubernetes manifests
  3. Deploys the updated application code

### Helm Chart

- The application uses Helm for Kubernetes deployments
- Helm is used for the Development deployment of the application.
- Helm charts define the application's GKE resources.
- Configuration files are located in the `helm` directory
- More details are in the README.md in the `helm` directory.

### Container Startup Process

The application uses an entrypoint script and start script to initialize the container.

#### Entrypoint Script (`compose/production/django/entrypoint`)

The entrypoint script runs first and handles database connectivity:

1. Sets PostgreSQL connection defaults
2. Constructs the `DATABASE_URL` environment variable
3. Waits for PostgreSQL to become available using `wait-for-it`
4. Passes control to the start script

#### Start Script

**Production** (`compose/production/django/start`):

1. `collectstatic` - Collects static files for serving
2. `migrate` - Applies database migrations
3. `ensure_adhs_organization` - Creates the default ADHS organization if it doesn't exist
4. `setup_permission_groups` - Creates/updates permission groups and their associated permissions
5. `seed_metadata_templates`, `seed_pathogens`, `seed_validation_rules` - Seeds the metadata vocabulary, in that order
6. Starts Gunicorn WSGI server on port 8000

**Local Development** (`compose/local/django/start`):

1. `migrate` - Applies database migrations
2. `ensure_adhs_organization` - Creates the default ADHS organization
3. `setup_permission_groups` - Creates/updates permission groups
4. `seed_metadata_templates`, `seed_pathogens`, `seed_validation_rules` - Seeds the metadata vocabulary, in that order
5. Starts Django development server with `runserver_plus` on port 8000

#### Key Management Commands

| Command                    | Description                                                                                                 |
| -------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `ensure_adhs_organization` | Creates the default ADHS organization required for the platform                                             |
| `setup_permission_groups`  | Creates all permission groups (Platform Admin, Lab Director, etc.) with their associated Django permissions |
| `seed_metadata_templates`  | Seeds/updates metadata templates, keys, values, and source types for file metadata                          |
| `seed_pathogens`           | Seeds the Pathogen registry with reportable pathogens (also populates the pathogen dropdown)                |
| `seed_validation_rules`    | Seeds/updates field- and cross-field validation rules for metadata templates                                |

> Both start scripts run these three on every container start, so a normal setup needs none of them by hand. Order matters: `seed_metadata_templates` first (it creates the keys, source types, and the pathogen key/template), then `seed_pathogens`, then `seed_validation_rules`.

### Metadata Template Seeding

The application uses a configurable metadata template system for tagging files and datasets with structured metadata. The `seed_metadata_templates` management command populates and updates the database with predefined metadata schemas.

#### Running the Command

```bash
docker compose -f docker-compose.local.yml run django python manage.py seed_metadata_templates
```

#### Data Model Overview

The metadata system consists of several interconnected models:

| Model                    | Location                                    | Purpose                                                                      |
| ------------------------ | ------------------------------------------- | ---------------------------------------------------------------------------- |
| `Key`                    | `asu_apgap/metadatatags/models.py`          | Predefined metadata field names with data types (TEXT, NUMBER, DATE, SELECT) |
| `Value`                  | `asu_apgap/metadatatags/models.py`          | Predefined values that can be assigned to keys (e.g., dropdown options)      |
| `SourceType`             | `asu_apgap/metadata_requirements/models.py` | Sample source categories (Human Host, Water Sample, etc.)                    |
| `MetadataTemplate`       | `asu_apgap/metadata_requirements/models.py` | Defines which keys apply to which source types, with requirement rules       |
| `MetadataTemplateOption` | `asu_apgap/metadata_requirements/models.py` | Links predefined values to templates for select/multi-select fields          |

#### How the Seeding Works

The management command (`asu_apgap/metadatatags/management/commands/seed_metadata_templates.py`) performs the following operations in a single atomic transaction:

1. **Key Rename Migration**: Moves existing user data from any keys listed in `KEY_RENAMES` onto their new names before new keys are created

2. **Source Types Creation**: Creates 12 predefined source types (Human Host, Companion Animal Host, Wildlife Host, Vectors, Livestock AG Animal Host, Air, Produce AG, Food Product, Surface, Soil Sample, Water Sample, Wastewater Sample)

3. **Keys & Values Collection**: Collects all unique metadata keys and values from three data structures:
   - `ALL_SEQUENCES`: Core metadata fields that apply to **all** source types (e.g., Sample ID, Pathogen name, Date Collected, Sequencing instrument)
   - `SOURCE_TYPE_METADATA`: Source-type-specific fields (e.g., "Biospecimen type" for Human Host, "Water source" for Water Sample)
   - `POST_ANALYSIS_CORE`: Fields for post-analysis templates

4. **Bulk Key Creation**: Creates `Key` objects with normalized names (uppercase, trimmed) and appropriate data types mapped from field types:
   - `text`, `text_field`, `text_input` → `TEXT`
   - `select`, `multi_select` → `SELECT`
   - `date`, `time` → `DATE`
   - `number` → `NUMBER`

5. **Bulk Value Creation**: Creates `Value` objects for all predefined dropdown/select options. The "Sequencing lab (originating lab)" options come from the active labs in the database rather than a fixed list

6. **Template Creation**: Creates `MetadataTemplate` records that define:
   - Which key applies to which source type (or `None` for core templates)
   - Whether the field is required
   - Whether multiple values can be selected
   - Display sort order
   - The UI field type (select, multi_select, text, etc.)

7. **Template Options Creation**: Links predefined `Value` objects to their corresponding `MetadataTemplate` records for select/multi-select fields

8. **Option Alias Merging**: Merges any alternate spellings a field declares in its `aliases` map onto the matching template options

9. **Stale Data Cleanup**: Removes keys and templates that are no longer in the seed data, skipping any that user-submitted metadata still references

10. **Pathogen Key Flagging**: Flags the seed field marked `is_pathogen_key`, which is the key the data catalogue's pathogen column and filter resolve

#### Data Structure Definition

The metadata schemas are defined as Python dictionaries in the management command file:

```python
# Core fields applied to ALL sequences (source_type=None)
ALL_SEQUENCES = {
    "keys": [
        {"name": "Sample ID", "required": False, "type": "text", "values": []},
        {
            "name": "Pathogen/organism name (or metagenomic)",
            "required": True,
            "type": "multi_select",
            "is_pathogen_key": True,
            "values": ["SARS-CoV-2", "Influenza", ...],
        },
        {"name": "Date Collected", "required": True, "type": "date", "values": []},
        # ... more fields
    ]
}

# Source-type specific metadata requirements
SOURCE_TYPE_METADATA = {
    "HUMAN_HOST": {
        "keys": [
            {"name": "Biospecimen type", "required": True, "type": "select", "values": ["Nasopharyngeal swab", "Saliva", ...]},
            {"name": "Age (years)", "required": False, "type": "number", "values": []},
            # ... more fields
        ]
    },
    "WATER_SAMPLE": {
        "keys": [
            {"name": "Water source", "required": True, "type": "select", "values": ["Municipal tap", "Irrigation line", ...]},
            {"name": "pH", "required": True, "type": "number", "values": []},
            # ... more fields
        ]
    },
    # ... more source types
}
```

#### Idempotent Behavior

The command is designed to be run multiple times safely:

- Existing records are updated if their properties have changed
- New records are created only if they don't exist
- Uses `ignore_conflicts=True` on bulk creates to handle race conditions
- All operations are wrapped in a database transaction

#### Modifying Metadata Templates

To add or modify metadata templates:

1. Edit the `ALL_SEQUENCES` dictionary for core fields that apply to all source types
2. Edit the `SOURCE_TYPE_METADATA` dictionary for source-type-specific fields
3. Run the management command to apply changes:
   ```bash
   docker compose -f docker-compose.local.yml run django python manage.py seed_metadata_templates
   ```

The command will output a summary of created/updated records upon completion.

### Sample Data

Seeding gives you the metadata vocabulary, but no labs, projects, or files. A fresh local database is therefore empty, and most of the UI has nothing to show. `populate_dummy_data` fills it with generated organizations, labs, projects, datasets, files, metadata tags, and requests to develop against:

```bash
docker compose -f docker-compose.local.yml run django python manage.py populate_dummy_data --count 5
```

This is a local development aid and has no part in any deployment. It re-runs `seed_metadata_templates` and `seed_pathogens` before generating, so the files it creates are tagged against the real vocabulary rather than look-alike keys; both are idempotent, so the repeat costs nothing.

The command names the database it is about to write to and asks you to confirm before it creates anything, so run it from an interactive terminal. If stdin is closed (in CI, or with stdin redirected from `/dev/null`), it reads that as a no and aborts rather than proceeding unattended.

`--count` is a multiplier, not a row count. At 5 you get 15 labs, around 50 projects, and around 150 files, which is enough to exercise every screen. The per-lab and per-project numbers are randomised, so counts vary slightly between runs. Larger values scale every table.

`--clear` wipes the generated data before repopulating, which is how you re-run it at a different `--count`. It is guarded twice: the command refuses to clear unless `DEBUG` is on, which it is in local settings and is not in any deployed environment, and it makes you type the database name at a second prompt before anything is deleted.

Your superuser survives a `--clear`, but every domain allowlist entry is deleted and only `asu.edu`, `azdhs.gov`, `tgen.org`, `arizona.edu`, and `ua.edu` come back. If you allowed another domain to create your superuser (`gmail.com`, for instance), add it back afterwards.

