from base64 import b64decode
from typing import Any, Dict, List, Union

from openai import AzureOpenAI

from core.tools.entities.tool_entities import ToolInvokeMessage
from core.tools.tool.builtin_tool import BuiltinTool


class GPT4VTool(BuiltinTool):
    def _invoke(self,
                user_id: str,
                tool_parameters: Dict[str, Any],
                ) -> Union[ToolInvokeMessage, List[ToolInvokeMessage]]:
        """
            invoke tools
        """
        client = AzureOpenAI(
            api_version=self.runtime.credentials['azure_openai_api_version'],
            azure_endpoint=self.runtime.credentials['azure_openai_base_url'],
            api_key=self.runtime.credentials['azure_openai_api_key'],
        )

        # image url
        image_url = tool_parameters.get('image_url', '')
        if not image_url:
            return self.create_text_message('Please input image')
        # prompt content
        content = tool_parameters.get('content', '')
        if not content:
            return self.create_text_message('Please input what your question about the image.')

        # call openapi gpt4-vision
        model = self.runtime.credentials['azure_openai_api_model_name']
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "You are a helpful assistant."},
                {"role": "user", "content": [
                    {
                        "type": "text",
                        "text": f"{content}"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"{image_url}"
                        }
                    }
                ]},
            ]
        )

        result = response.choices[0].message.content

        return result
