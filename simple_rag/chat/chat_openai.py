from openai import OpenAI
import os
import json
from dotenv import load_dotenv
import json

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
        temperature=0.1,
        top_p=0.95,
        max_tokens=1024,
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
        message = [
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
            messages=message,
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
            "output": fine_output,
            "completion_tokens": response.usage.completion_tokens,
            "prompt_tokens": response.usage.prompt_tokens,
            "total_tokens": response.usage.total_tokens,
        }
        return result
