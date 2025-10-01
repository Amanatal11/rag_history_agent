import os
import requests
from bs4 import BeautifulSoup
from logger import logger

def fetch_and_save_page(title, data_dir="data"):
    """
    Fetch Wikipedia page and save main content as .txt.
    """
    url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = "\n".join([p.get_text() for p in paragraphs])
        if not text.strip():
            logger.warning(f"No content found for {title}")
            return None
        os.makedirs(data_dir, exist_ok=True)
        file_path = os.path.join(data_dir, f"{title}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)
        logger.info(f"Saved page '{title}' to {file_path}")
        return file_path
    except Exception as e:
        logger.error(f"Failed to fetch '{title}': {e}")
        return None