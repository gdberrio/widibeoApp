import requests
import json
import dateutil.parser
import airbyte
from airbyte.models import operations, shared
import json


class AirbyteAuthService:
    def __init__(self, airbyte_token) -> None:
        self.airbyte_token = airbyte_token
        self.s = airbyte.Airbyte(
            security=shared.Security(bearer_auth=self.airbyte_token)
        )


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
    host: str,
    port: int,
    database: str,
    username: str,
    password: str,
) -> operations.CreateSourceResponse:
    req = shared.SourceCreateRequest(
        configuration=shared.SourcePostgres(
            host=host,
            port=port,
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


def get_google_ads_consent_url(
    airbyte_auth: AirbyteAuthService, workspace_id: str
) -> str:
    req = shared.InitiateOauthRequest(
        name=shared.OAuthActorNames.GOOGLE_ADS,
        o_auth_input_configuration=shared.OAuthInputConfiguration(),
        redirect_url="https://3626-213-122-179-210.ngrok-free.app/oauth_callback",
        workspace_id=workspace_id,
    )

    res = airbyte_auth.s.sources.initiate_o_auth(req)

    if res.status_code != 200:
        return "error: oauth call failed"
    consent_url = json.loads(res.raw_response.content.decode())["consentUrl"]  # type: ignore
    return consent_url


def create_google_ads_source(
    airbyte_auth: AirbyteAuthService,
    workspace_id: str,
    secret_id: str,
    customer_id="6597976726",
    manager_customer_id="9831493179",
) -> operations.CreateSourceResponse:
    req = shared.SourceCreateRequest(
        configuration=shared.SourceGoogleAds(
            credentials=shared.GoogleAdsCredentials(),  # type: ignore
            customer_id=customer_id,
            start_date=dateutil.parser.isoparse("2023-08-18T00:00:00Z"),
            source_type=shared.SourceGoogleAdsGoogleAds.GOOGLE_ADS,
            login_customer_id=manager_customer_id,
            conversion_window_days=30,
        ),
        name="google ads test account",
        secret_id=secret_id,
        workspace_id=workspace_id,
    )

    res = airbyte_auth.s.sources.create_source(req)

    return res


def create_azure_destination(
    airbyte_auth: AirbyteAuthService,
    workspace_id: str,
    azure_blob_storage_account_key: str,
    azure_blob_storage_account_name: str,
) -> operations.CreateDestinationResponse:
    req = shared.DestinationCreateRequest(
        configuration=shared.DestinationAzureBlobStorage(
            azure_blob_storage_account_key=azure_blob_storage_account_key,
            azure_blob_storage_account_name=azure_blob_storage_account_name,
            destination_type=shared.DestinationAzureBlobStorageAzureBlobStorage.AZURE_BLOB_STORAGE,
            format=shared.DestinationAzureBlobStorageFormatCSVCommaSeparatedValues(
                flattening=shared.DestinationAzureBlobStorageFormatCSVCommaSeparatedValuesNormalizationFlattening.ROOT_LEVEL_FLATTENING,
                format_type=shared.DestinationAzureBlobStorageFormatCSVCommaSeparatedValuesFormatType.CSV,
            ),
        ),
        name="azure test storage",
        workspace_id=workspace_id,
    )

    res = airbyte_auth.s.destinations.create_destination(req)

    return res


def create_s3_destination(
    airbyte_auth: AirbyteAuthService,
    workspace_id: str,
    aws_access_key: str,
    aws_access_secret: str,
    s3_bucket_name: str,
    s3_bucket_path: str,
    s3_bucket_region: shared.DestinationS3S3BucketRegion = shared.DestinationS3S3BucketRegion.EU_WEST_2,
) -> operations.CreateDestinationResponse:
    req = shared.DestinationCreateRequest(
        configuration=shared.DestinationS3(
            destination_type=shared.DestinationS3S3.S3,
            access_key_id=aws_access_key,
            secret_access_key=aws_access_secret,
            format=shared.DestinationS3FormatParquetColumnarStorage(
                format_type=shared.DestinationS3FormatParquetColumnarStorageFormatType.PARQUET,
            ),
            s3_bucket_name=s3_bucket_name,
            s3_bucket_path=s3_bucket_path,
            s3_bucket_region=s3_bucket_region,
        ),
        name="S3 Datalake",
        workspace_id=workspace_id,
    )

    res = airbyte_auth.s.destinations.create_destination(req)

    return res


def get_stream_properties(
    airbyte_auth: AirbyteAuthService,
    source_id: str,
    destination_id: str,
    ignore_cache: str = "false",
):
    url = f"https://api.airbyte.com/v1/streams?sourceId={source_id}&destinationId={destination_id}&ignoreCache={ignore_cache}"

    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {airbyte_auth.airbyte_token}",
    }

    response = requests.get(url, headers=headers)

    data = json.loads(response.content)
    return data


def create_connection(
    airbyte_auth: AirbyteAuthService,
    source_id: str,
    destination_id: str,
) -> operations.CreateConnectionResponse:
    req = shared.ConnectionCreateRequest(
        source_id=source_id, destination_id=destination_id, name="test destination"
    )

    res = airbyte_auth.s.connections.create_connection(req)
    return res
