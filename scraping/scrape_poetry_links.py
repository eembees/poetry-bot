import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from time import sleep
from typing import List, Dict, Union

from bs4 import BeautifulSoup
from selenium import webdriver


@dataclass
class Book:
    title: str
    id: str
    url: str


def get_book_from_link(link) -> Union[Book, None]:
    bk = None
    try:
        if "ebook" in link["title"]:
            bk = Book(title=link.text, id=link["title"], url=link["href"])
    except KeyError:
        pass
    return bk


def parse(page_source) -> List:
    books = []
    soup = BeautifulSoup(page_source, "html.parser")
    for link in soup.find_all("a"):  # Find all external links
        books.append(get_book_from_link(link))
    return books


def main(args: Dict):
    output_file = args["output"]
    url = args["url"]
    print("Starting - loading URL")
    # create a new Firefox session
    driver = webdriver.Safari()
    driver.implicitly_wait(30)
    driver.get(url)
    print("Now waiting for some time....")

    sleep(1)

    books = parse(driver.page_source)

    driver.quit()

    # Data cleanup - remove nones and clean author names
    books = [b.__dict__ for b in books if b is not None]

    print(json.dumps(books, indent=4, ensure_ascii=False))
    print(f"FOUND {len(books)} BOOKS")
    print("Saving to  ")
    print(output_file)

    with output_file.open("w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=4)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Scrape all ebooks from a given gutenberg bookshelf."
    )
    parser.add_argument(
        "--url",
        type=str,
        default="http://www.gutenberg.org/wiki/Poetry_(Bookshelf)",
        help="URL to scrape",
    )
    parser.add_argument(
        "--output",
        default="./output/books.json",
        type=str,
        help="File to output JSON to.",
    )

    args = parser.parse_args()
    argdict = vars(args)
    argdict["output"] = Path(argdict["output"])
    argdict["output"].parent.mkdir(exist_ok=True)

    return argdict


if __name__ == "__main__":
    args = parse_args()
    main(args)
