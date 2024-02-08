from typing import Any, Dict

from core.tools.errors import ToolProviderCredentialValidationError
from core.tools.provider.builtin.azuredalle.tools.gpt4v import GPT4VTool
from core.tools.provider.builtin_tool_provider import BuiltinToolProviderController


class AzureGPT4VProvider(BuiltinToolProviderController):
    def _validate_credentials(self, credentials: Dict[str, Any]) -> None:
        try:
            GPT4VTool().fork_tool_runtime(
                meta={
                    "credentials": credentials,
                }
            ).invoke(
                user_id='',
                tool_parameters={
                    "img_url": "<image URL>",
                    "content": "describe the image",
                },
            )
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
