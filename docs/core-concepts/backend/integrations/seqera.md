# Seqera

[Seqera Platform](https://cloud.seqera.io) is where bioinformatics users launch and monitor
Nextflow pipelines. The backend doesn't run pipelines itself. It creates a Seqera workspace
per project, along with the credentials, compute environment, and data links that workspace
needs, keeps project members in sync as workspace participants, and links users into Seqera
from the project detail page.

## Setup

The Seqera integration requires a Seqera organization and an access token given to the
django backend that allows interacting with the Seqera Platform API.

1. **Sign into an account that is an owner on the organization.** In Seqera, access tokens are
tied to a user account, so this must be done on an account that will not leave the organization.

2. **Create a personal access token.** Go to
[cloud.seqera.io/tokens](https://cloud.seqera.io/tokens), make sure you are signed in to the correct
account, and click **Add token**. Name it for the environment, e.g. `APGAP UAT`.

    !!! warning "Warning"

        Make sure to copy the token, you can only do this once. The token is a secret that allows
        access to anything the user account can access, do not share it publicly.

    ![Placeholder: Seqera "Your tokens" page with the Add token dialog open](/images/seqera-integration-add-pat.png)

3. **Find the organization ID.** We need the numeric `orgId`, which the Seqera UI never shows,
so ask the API using the token you just made:

    ```bash
    curl -s -H "Authorization: Bearer <token>" https://api.cloud.seqera.io/orgs
    ```

    This returns every organization the account can see. Take the `orgId` of the intended
    organization. Check that its `memberRole` reads `owner` while you're there.

4. **Store both** in the app secrets, as `SEQERA_API_TOKEN` and `SEQERA_ORGANIZATION_ID`.


