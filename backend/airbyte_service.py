import airbyte
from airbyte.models import operations, shared
from dotenv import load_dotenv
import os

load_dotenv()
airbyte_key = os.getenv("airbyte_key")


class AirbyteService:
    def __init__(self, airbyte_token) -> None:
        self.airbyte_token = airbyte_token
        self.s = airbyte.Airbyte(
            security=shared.Security(bearer_auth=self.airbyte_token)
        )
        self.workspace_id = None

    def list_workspaces(self) -> operations.ListWorkspacesResponse:
        req = operations.ListWorkspacesRequest()
        res = self.s.workspaces.list_workspaces(req)
        return res

    def create_workspace(
        self, workspace_name: str
    ) -> operations.CreateWorkspaceResponse:
        req = shared.WorkspaceCreateRequest(name=workspace_name)

        res = self.s.workspaces.create_workspace(req)

        if res is not None:
            self.workspace_id = res.workspace_response.workspace_id

        return res
