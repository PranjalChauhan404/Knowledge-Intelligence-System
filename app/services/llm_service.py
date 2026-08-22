import os
import time

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class LLMService:

    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        self.max_retries = 3


    def generate_response(self, prompt):

        for attempt in range(self.max_retries):

            try:

                response = self.client.responses.create(
                    model="gpt-5-mini",
                    input=prompt
                )

                return response.output_text


            except Exception as error:

                # Last attempt: let the error propagate
                if attempt == self.max_retries - 1:
                    raise

                # Short exponential backoff:
                # attempt 1 → 1 second
                # attempt 2 → 2 seconds
                wait_time = 2 ** attempt

                print(
                    f"LLM request failed. "
                    f"Retrying in {wait_time}s..."
                )

                time.sleep(wait_time)