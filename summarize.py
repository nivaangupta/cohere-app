from pdfminer.high_level import extract_text
import cohere
from dotenv import load_dotenv
import os

load_dotenv()
key = os.environ.get("api_key")

co = cohere.Client(key)
# filePath = "./uploads/Temperature_actuated_non-touch_automatic_door.pdf"


class Summary:
    def extractText(self, filePath):
        return extract_text(filePath)

    def summarize(self, path):
        response = co.summarize(
            text=self.extractText(path),
            model='command',
            length='medium',
            extractiveness='medium'
        )
        return response.summary
