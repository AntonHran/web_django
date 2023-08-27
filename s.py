import os
import configparser
from pathlib import Path

import django
from pymongo import MongoClient
from django.db.utils import IntegrityError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quotes_site.settings")
django.setup()

from quotes.models import Author, Quote, Tag, MtM

config_path: Path = Path(__file__).parent.joinpath("config.ini")
config = configparser.ConfigParser()
config.read(config_path)

username: str = config.get('DB', 'username')
password: str = config.get('DB', 'password')
db_name: str = config.get('DB', 'db_name')
domain: str = config.get('DB', 'domain')
flag: str = config.get('DB', 'flag')

url: str = f"mongodb+srv://{username}:{password}@{domain}/{flag}"
client = MongoClient(url)
db = getattr(client, db_name)

empty_tag = "without tag"


def seed_authors():
    authors = db.author.find()
    if authors:
        for author in authors:
            try:
                Author(
                    full_name=author["full_name"],
                    birth_date=author["born_date"],
                    birth_place=author["born_location"],
                    biography=author["description"],
                ).save()
            except IntegrityError:
                continue


def seed_quotes():
    quotes = db.quote.find()
    authors = Author.objects.all()
    if quotes:
        for quote_ in quotes:
            print(quote_)
            try:
                Quote(
                    quote=quote_["quote"],
                    author=get_author(quote_["author"], authors),
                ).save()
            except IntegrityError:
                continue
            q = Quote.objects.get(quote=quote_["quote"])
            write_relation(quote_["tags"], q)


def get_author(object_id: str, authors_postgres) -> int | None:
    for author_mongo in db.author.find():
        if author_mongo["_id"] == object_id:
            for author_postgres in authors_postgres:
                if author_postgres.full_name == author_mongo["full_name"]:
                    return author_postgres
    return None


def get_tags(tag: str):
    tags = [el["name"] for el in Tag.objects.values("name")]
    if tag not in tags:
        Tag(name=tag).save()


def write_relation(tags: list[str], quote: Quote) -> None:
    for tag in tags:
        if tag:
            get_tags(tag)
            MtM(quote=quote, tag=Tag.objects.get(name=tag)).save()
        else:
            MtM(quote=quote, tag=Tag.objects.get(name=empty_tag)).save()


if __name__ == '__main__':
    Tag(name=empty_tag).save()
    seed_authors()
    seed_quotes()
