import logging
import quopri
from datetime import datetime

import requests
from bs4 import BeautifulSoup

try:
    from llama_index import download_loader
except ImportError:
    raise ImportError("Notion requires extra dependencies. Install with `pip install embedchain[community]`") from None

from embedchain.loaders.base_loader import BaseLoader
from embedchain.utils import clean_string


def get_header(text: str, header: str) -> str:
    start_string_position = text.find(header)
    pos_start = text.find(":", start_string_position) + 1
    pos_end = text.find("\n", pos_start)
    header = text[pos_start:pos_end]
    return header.strip()


class GmailLoader(BaseLoader):
    def load_data(self, query):
        """Load data from gmail."""

        GmailReader = download_loader("GmailReader")
        loader = GmailReader(query=query)
        documents = loader.load_data()
        logging.info(f"Gmail Loader: {len(documents)} mails found")

        output = []
        for document in documents:
            original_size = len(document.text)

            snippet = document.metadata.get("snippet")
            meta_data = {
                "url": document.metadata.get("id"),
                "date": get_header(document.text, "Date"),
                "subject": get_header(document.text, "Subject"),
                "from": get_header(document.text, "From"),
                "to": get_header(document.text, "To"),
                "search_query": query,
            }

            # Decode
            decoded_bytes = quopri.decodestring(document.text)
            decoded_str = decoded_bytes.decode("utf-8", errors="replace")

            # Slice
            mail_start = decoded_str.find("<!DOCTYPE")
            data = decoded_str[mail_start:]

            # Web Page HTML Processing
            soup = BeautifulSoup(data, "html.parser")

            tags_to_exclude = [
                "nav",
                "aside",
                "form",
                "header",
                "noscript",
                "svg",
                "canvas",
                "footer",
                "script",
                "style",
            ]
            for tag in soup(tags_to_exclude):
                tag.decompose()

            ids_to_exclude = ["sidebar", "main-navigation", "menu-main-menu"]
            for id in ids_to_exclude:
                tags = soup.find_all(id=id)
                for tag in tags:
                    tag.decompose()

            classes_to_exclude = [
                "elementor-location-header",
                "navbar-header",
                "nav",
                "header-sidebar-wrapper",
                "blog-sidebar-wrapper",
                "related-posts",
            ]
            for class_name in classes_to_exclude:
                tags = soup.find_all(class_=class_name)
                for tag in tags:
                    tag.decompose()

            content = soup.get_text()
            content = clean_string(content)

            cleaned_size = len(content)
            if original_size != 0:
                logging.info(
                    f"[{id}] Cleaned page size: {cleaned_size} characters, down from {original_size} (shrunk: {original_size-cleaned_size} chars, {round((1-(cleaned_size/original_size)) * 100, 2)}%)"  # noqa:E501
                )

            result = f"email from '{meta_data.get('from')}' to '{meta_data.get('to')}'\nsubject: {meta_data.get('subject')}\ndate: {meta_data.get('date')}\npreview: {snippet}\ncontent: f{content}\n"
            output.append({"meta_data": meta_data, "content": result})

        return output