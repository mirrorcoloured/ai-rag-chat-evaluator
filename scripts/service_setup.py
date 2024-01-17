import logging
import os

from azure.core.credentials import AzureKeyCredential
from azure.identity import AzureDeveloperCliCredential
from azure.search.documents import SearchClient

logger = logging.getLogger("scripts")


def get_openai_config():
    if os.environ.get("OPENAI_HOST") == "azure":
        if os.environ.get("AZURE_OPENAI_KEY"):
            logger.info("Using Azure OpenAI Service with API Key from AZURE_OPENAI_KEY")
            api_type = "azure"
            api_key = os.environ["AZURE_OPENAI_KEY"]
        else:
            logger.info("Using Azure OpenAI Service with Azure Developer CLI Credential")
            api_type = "azure_ad"
            azure_credential = AzureDeveloperCliCredential()
            api_key = azure_credential.get_token("https://cognitiveservices.azure.com/.default").token
        openai_config = {
            "api_type": api_type,
            "api_base": f"https://{os.environ['AZURE_OPENAI_SERVICE']}.openai.azure.com",
            "api_key": api_key,
            "api_version": "2023-07-01-preview",
            "deployment_id": os.environ["AZURE_OPENAI_EVAL_DEPLOYMENT"],
            "model": os.environ["OPENAI_GPT_MODEL"],
        }
    else:
        logger.info("Using OpenAI Service with API Key from OPENAICOM_KEY")
        openai_config = {
            "api_type": "openai",
            "api_key": os.environ["OPENAICOM_KEY"],
            "organization": os.environ["OPENAICOM_ORGANIZATION"],
            "model": os.environ["OPENAI_GPT_MODEL"],
        }
    return openai_config


def get_search_client():
    if api_key := os.environ.get("AZURE_SEARCH_KEY"):
        logger.info("Using Azure Search Service with API Key from AZURE_SEARCH_KEY")
        azure_credential = AzureKeyCredential(api_key)
    else:
        logger.info("Using Azure Search Service with Azure Developer CLI Credential")
        azure_credential = AzureDeveloperCliCredential()

    return SearchClient(
        endpoint=f"https://{os.environ['AZURE_SEARCH_SERVICE']}.search.windows.net",
        index_name=os.environ["AZURE_SEARCH_INDEX"],
        credential=azure_credential,
    )