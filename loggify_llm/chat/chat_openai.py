from openai import OpenAI
import os
import json
from dotenv import load_dotenv
import json
import base64
import requests
from IPython.display import Image, display

load_dotenv()


class ChatOpenAI:
    """
    A class to interact with OpenAI's language model for generating chat responses.

    Attributes:
        llm_model (str): The language model to use, default is "gpt-3.5-turbo".
        client (OpenAI): The OpenAI client initialized with the API key.

    Methods:
        request(prompt: str, question: str, temperature: float, top_p: float, max_tokens: int, **kwargs):
            Sends a request to the OpenAI API with the provided prompt and question, and returns the response.
    """

    def __init__(self, llm_model: str = "gpt-3.5-turbo"):
        """
        Initializes the ChatOpenAI class with the specified language model.

        Args:
            llm_model (str): The language model to use. Default is "gpt-3.5-turbo".
        """
        super().__init__()
        open_api_key = os.environ.get("OPENAI_API_KEY")
        assert open_api_key, "OPENAI_API_KEY environment variable not set"
        self.client = OpenAI(api_key=open_api_key)
        self.llm_model = llm_model

    def request(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.1,
        top_p: float = 0.95,
        max_tokens: int = 1024,
        **kwargs,
    ):
        """
        Sends a request to the OpenAI API with the provided system prompt and user prompt.

        Args:
            system_prompt (str): The system prompt to set the context.
            user_prompt (str): The user's question to get a response for.
            temperature (float): Sampling temperature to control the randomness of the response. Default is 0.1.
            top_p (float): The cumulative probability of token selection. Default is 0.95.
            max_tokens (int): The maximum number of tokens to generate. Default is 1024.
            **kwargs: Additional arguments to pass to the OpenAI API.

        Returns:
            dict: A dictionary containing the request ID, output, completion tokens, prompt tokens, and total tokens.
        """
        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ]
        response = self.client.chat.completions.create(
            messages=messages,
            model=self.llm_model,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            **kwargs,
        )
        raw_output = response.choices[0].message.content
        try:
            fine_output = json.loads(raw_output)
        except Exception as e:
            print(f"👾 Warning: Failed to refine the output of LLM because: {e}")
            fine_output = raw_output

        result = {
            "request_id": response.id,
            "llm_model": self.llm_model,
            "input": messages,
            "output": fine_output,
            "completion_tokens": response.usage.completion_tokens,
            "prompt_tokens": response.usage.prompt_tokens,
            "total_tokens": response.usage.total_tokens,
        }
        return result


class ChatOpenAIVision:
    """
    A class to interact with OpenAI's vision-enhanced language model for generating responses based on text and images.

    Attributes:
        llm_model (str): The language model to use, default is "gpt-4-vision-preview".
        headers (dict): The headers for the OpenAI API requests.
        client (OpenAI): The OpenAI client initialized with the API key.

    Methods:
        encode_image(image_path):
            Encodes an image file to a base64 string.

        question_image(url, user_prompt, max_tokens=1024, temperature=1e-4):
            Sends a request to the OpenAI API with the provided prompt and image URL or file path, and returns the response.
    """

    def __init__(self, llm_model: str = "gpt-4-vision-preview"):
        """
        Initializes the ChatVision class with the specified language model.

        Args:
            llm_model (str): The language model to use. Default is "gpt-4-vision-preview".
        """
        open_api_key = os.environ.get("OPENAI_API_KEY")
        assert open_api_key, "OPENAI_API_KEY environment variable not set"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {open_api_key}",
        }
        self.client = OpenAI(api_key=open_api_key)
        self.llm_model = llm_model

    def encode_image(self, image_path):
        """
        Encodes an image file to a base64 string.

        Args:
            image_path (str): The path to the image file.

        Returns:
            str: The base64-encoded string of the image.
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def request(
        self,
        image_url: str,
        user_prompt: str,
        max_tokens: int = 1024,
        temperature: float = 1e-4,
        show_preview: bool = False,
    ):
        """
        Sends a request to the OpenAI API with the provided prompt and image URL or file path, and returns the response.

        Args:
            image_url (str): The URL of the image or the local file path to the image.
            user_prompt (str): The prompt or question to ask the model.
            max_tokens (int): The maximum number of tokens to generate. Default is 1024.
            temperature (float): Sampling temperature to control the randomness of the response. Default is 1e-4.

        Returns:
            dict: A dictionary containing the request ID, output, completion tokens, prompt tokens, and total tokens.
        """

        if "http" in image_url:
            if show_preview:
                display(Image(url=image_url))
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"{user_prompt}"},
                        {
                            "type": "image_url",
                            "image_url": image_url,
                        },
                    ],
                }
            ]
            response = self.client.chat.completions.create(
                model=self.llm_model,
                messages=messages,
                max_tokens=max_tokens,
            )
        else:
            if show_preview:
                display(Image(filename=image_url))
            base64_image = self.encode_image(image_url)
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"{user_prompt}?"},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                        },
                    ],
                }
            ]
            payload = {
                "model": self.llm_model,
                "temperature": temperature,
                "messages": messages,
                "max_tokens": max_tokens,
            }
            response = requests.post(
                url="https://api.openai.com/v1/chat/completions",
                headers=self.headers,
                json=payload,
            )
            response = response.json()
            response = DotDict(response)

        raw_output = response.choices[0].message.content
        try:
            fine_output = json.loads(raw_output)
        except Exception as e:
            print(f"👾 Warning: Failed to refine the output of LLM because: {e}")
            fine_output = raw_output

        result = {
            "request_id": response.id,
            "llm_model": self.llm_model,
            "input": messages,
            "output": fine_output,
            "completion_tokens": response.usage.completion_tokens,
            "prompt_tokens": response.usage.prompt_tokens,
            "total_tokens": response.usage.total_tokens,
        }
        return result


class DotDict(dict):
    """A dictionary with dot notation access."""

    def __getattr__(self, item):
        try:
            value = self[item]
            if isinstance(value, dict):
                return DotDict(value)
            if isinstance(value, list):
                return [DotDict(x) if isinstance(x, dict) else x for x in value]
            return value
        except KeyError:
            raise AttributeError(f"No such attribute: {item}")
