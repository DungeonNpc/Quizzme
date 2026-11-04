import time
from openai import OpenAI, APIStatusError, APIConnectionError
from app.config import API_KEY, BASE_URL, MODEL

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

RETRY_STATUS = {429, 500, 502, 503, 504}


def call_llm(system: str, user: str, temperature: float = 0.3, retries: int = 4) -> str:
    for attempt in range(retries + 1):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                temperature=temperature,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            )
            return response.choices[0].message.content
        except APIStatusError as e:
            if e.status_code not in RETRY_STATUS or attempt == retries:
                raise
        except APIConnectionError:
            if attempt == retries:
                raise
        time.sleep(2 ** attempt)  # waits 1s, 2s, 4s, 8s


if __name__ == "__main__":
    print(call_llm("You are a helpful assistant.", "Say hello in one sentence."))