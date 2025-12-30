import requests

class Script_Generator:
    def __init__(self) -> None:
        self.url = "http://localhost:1234/v1/chat/completions"
        self.model = ""
        self.response = ""
        self.niche = ""

    def generate_script(self, model, niche) -> str:
        self.model = model
        self.niche = niche

        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "messages": [
                {
                    "role": "system",
                    "content": f"Can you write me a 50 word minimum script for this niche - {self.niche}"
                },
                ],
                "temperature": 0.7,
                "max_tokens": -1,
                "stream": False
            }
        )

        self.response = response.json()

        content = self.response["choices"][0]["message"]["content"]

        return content