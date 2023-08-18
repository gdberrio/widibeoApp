import airbyte
from airbyte.models import operations, shared
from dotenv import load_dotenv
import os

load_dotenv()
airbyte_key = os.getenv("airbyte_key")
testing_workspace_id = os.getenv("testing_workspace_id")
testing_google_ads_dev_token = os.getenv("google_ads_test_developer_token")
testing_google_ads_customer_id = os.getenv("google_ads_test_customer_id")


class AirbyteAuthService:
    def __init__(self, airbyte_token) -> None:
        self.airbyte_token = airbyte_token
        self.s = airbyte.Airbyte(
            security=shared.Security(bearer_auth=self.airbyte_token)
        )
        self.workspace_id = None


def list_workspaces(
    airbyte_auth: AirbyteAuthService,
) -> operations.ListWorkspacesResponse:
    req = operations.ListWorkspacesRequest()
    res = airbyte_auth.s.workspaces.list_workspaces(req)
    return res


def create_workspace(
    airbyte_auth: AirbyteAuthService, workspace_name: str
) -> operations.CreateWorkspaceResponse:
    req = shared.WorkspaceCreateRequest(name=workspace_name)

    res = airbyte_auth.s.workspaces.create_workspace(req)

    return res


def create_psql_source(
    airbyte_auth: AirbyteAuthService,
    workspace_id: str,
    name: str,
    database: str,
    username: str,
    password: str,
) -> operations.CreateSourceResponse:
    req = shared.SourceCreateRequest(
        configuration=shared.SourcePostgres(
            host="127.0.0.1",
            port=5432,
            database=database,
            username=username,
            password=password,
            source_type=shared.SourcePostgresPostgres.POSTGRES,
        ),
        name=name,
        workspace_id=workspace_id,
    )

    res = airbyte_auth.s.sources.create_source(req)

    return res
