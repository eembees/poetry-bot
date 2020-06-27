# coding=utf-8
import argparse
import json
from pathlib import Path
from typing import Dict, List

from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers


def get_book_ids(list_of_book_dicts: List[Dict], num: int = 5) -> List[int]:
    return [int(d["id"].replace("ebook:", "")) for d in list_of_book_dicts][
        :num
    ]


def write_a_book_to_file(id: int, filepath: Path) -> None:
    with filepath.open("a") as fp:
        fp.write(strip_headers(load_etext(id)).strip())


def parse_args():
    parser = argparse.ArgumentParser(
        description="Scrape all ebooks from a given gutenberg bookshelf to single."
    )
    parser.add_argument(
        "--output",
        default="./output/books.txt",
        type=str,
        help="JSON to read book ids from.",
    )

    parser.add_argument(
        "--input",
        default="./output/books.json",
        type=str,
        help="File to store all of the text.",
    )

    parser.add_argument(
        "--num", default=5, type=int, help="Number of books to scrape.",
    )

    args = parser.parse_args()
    argdict = vars(args)
    argdict["input"] = Path(argdict["input"])
    argdict["output"] = Path(argdict["output"])
    assert argdict["input"].exists()
    return argdict


def main(args: Dict):
    # read json
    with args["input"].open("r") as fp:
        list_of_dicts = json.load(fp)
    ids = get_book_ids(list_of_dicts, num=args["num"])
    args["output"].write_text(
        "Output from scraping books with ids: "
        + ", ".join([str(id) for id in ids])
        + "\n"
    )
    for id in ids:
        write_a_book_to_file(id, filepath=args["output"])
    print("Finished Downloading files.")
    print(f"{len(ids)} books printed to: ")
    print(args["output"])


if __name__ == "__main__":
    args = parse_args()
    main(args)
