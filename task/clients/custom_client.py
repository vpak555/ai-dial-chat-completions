import json
import aiohttp
import requests

from task.clients.base import BaseClient
from task.constants import DIAL_ENDPOINT
from task.models.message import Message
from task.models.role import Role


class CustomDialClient(BaseClient):
    _endpoint: str
    _api_key: str

    def __init__(self, deployment_name: str):
        super().__init__(deployment_name)
        self._endpoint = DIAL_ENDPOINT + f"/openai/deployments/{deployment_name}/chat/completions"

    def get_completion(self, messages: list[Message]) -> Message:
        #TODO:
        # Take a look at README.md of how the request and regular response are looks like!
        # 1. Create headers dict with api-key and Content-Type
        # 2. Create request_data dictionary with:
        #   - "messages": convert messages list to dict format using msg.to_dict() for each message
        # 3. Make POST request using requests.post() with:
        #   - URL: self._endpoint
        #   - headers: headers from step 1
        #   - json: request_data from step 2
        # 4. Get content from response, print it and return message with assistant role and content
        # 5. If status code != 200 then raise Exception with format: f"HTTP {response.status_code}: {response.text}"
        headers = {
            "api-key": self._api_key,
            "Content-Type": "application/json"
        }
        
        request_data = {
            "messages": [msg.to_dict() for msg in messages]
        }
        
        print(f"\n=== REQUEST ===")
        print(f"URL: {self._endpoint}")
        print(f"Headers: {headers}")
        print(f"Body: {json.dumps(request_data, indent=2)}")
        
        response = requests.post(
            self._endpoint,
            headers=headers,
            json=request_data
        )
        
        print(f"\n=== RESPONSE ===")
        print(f"Status: {response.status_code}")
        print(f"Body: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code != 200:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
        
        response_data = response.json()
        if not response_data.get('choices'):
            raise Exception("No choices in response found")
        
        content = response_data['choices'][0]['message']['content']
        print(f"\nAI: {content}")
        return Message(role=Role.AI, content=content)

    async def stream_completion(self, messages: list[Message]) -> Message:
        #TODO:
        # Take a look at README.md of how the request and streamed response chunks are looks like!
        # 1. Create headers dict with api-key and Content-Type
        # 2. Create request_data dictionary with:
        #    - "stream": True  (enable streaming)
        #    - "messages": convert messages list to dict format using msg.to_dict() for each message
        # 3. Create empty list called 'contents' to store content snippets
        # 4. Create aiohttp.ClientSession() using 'async with' context manager
        # 5. Inside session, make POST request using session.post() with:
        #    - URL: self._endpoint
        #    - json: request_data from step 2
        #    - headers: headers from step 1
        #    - Use 'async with' context manager for response
        # 6. Get content from chunks (don't forget that chunk start with `data: `, final chunk is `data: [DONE]`), print
        #    chunks, collect them and return as assistant message
        headers = {
            "api-key": self._api_key,
            "Content-Type": "application/json"
        }
        
        request_data = {
            "stream": True,
            "messages": [msg.to_dict() for msg in messages]
        }
        
        print(f"\n=== STREAM REQUEST ===")
        print(f"URL: {self._endpoint}")
        print(f"Headers: {headers}")
        print(f"Body: {json.dumps(request_data, indent=2)}")
        
        contents = []
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self._endpoint,
                json=request_data,
                headers=headers
            ) as response:
                print(f"\n=== STREAM RESPONSE ===")
                print(f"Status: {response.status}")
                print("AI: ", end='', flush=True)
                
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"HTTP {response.status}: {error_text}")
                
                async for line in response.content:
                    line_str = line.decode('utf-8').strip()
                    if line_str.startswith('data: '):
                        data_str = line_str[6:]  # Remove 'data: ' prefix
                        if data_str == '[DONE]':
                            break
                        
                        try:
                            chunk_data = json.loads(data_str)
                            content = self._get_content_snippet(chunk_data)
                            if content:
                                print(content, end='', flush=True)
                                contents.append(content)
                        except json.JSONDecodeError:
                            continue
        
        print()
        full_content = ''.join(contents)
        return Message(role=Role.AI, content=full_content)
    
    def _get_content_snippet(self, chunk_data: dict) -> str:
        """
        Extract content from a streaming chunk.
        Returns the content string or empty string if not present.
        """
        if 'choices' in chunk_data and chunk_data['choices']:
            choice = chunk_data['choices'][0]
            if 'delta' in choice and 'content' in choice['delta']:
                return choice['delta']['content']
        return ""

