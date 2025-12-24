import requests
import re

class Niche_Discovery:
    def __init__(self, model) -> None:
        self.url = "http://localhost:1234/v1/chat/completions"
        self.model = model
        self.response = ""
        self.niches = []
    
    def get_niches(self) -> str:
        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "messages": [
                {
                    "role": "system",
                    "content": "can you find me a list of the top currently trending story telling niches on youtube shorts, i dont want anything else simply just give me a list from 1-5 so i can easily parse it into my code"
                },
                ],
                "temperature": 0.7,
                "max_tokens": -1,
                "stream": False
            }
        )

        self.response = response.json()

        content = self.response["choices"][0]["message"]["content"]
        
        lines = content.strip().split('\n')
        for line in lines:
            match = re.match(r'^\d+[.\s]+(.+)$', line.strip())

            if match:
                niche = match.group(1).strip()
                if niche:  
                    self.niches.append(niche)
        

        return self.niches
