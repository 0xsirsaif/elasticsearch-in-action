import random
import os

import faker
from faker.providers import BaseProvider, person, date_time, currency
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch

fake = faker.Faker()


class Amazon(BaseProvider):
    def rate(self):
        return random.randint(1, 5)

    def is_best_seller(self):
        return random.choice([True, False])


class PriceList(BaseProvider):
    def price_list(self):
        return {
            fake.currency()[0]: fake.pricetag() for _ in range(random.randint(2, 5))
        }


fake.add_provider(person)
fake.add_provider(date_time)
fake.add_provider(currency)
fake.add_provider(Amazon)
fake.add_provider(PriceList)


def gen_fake_books(num_docs: int):
    for doc_id in range(1, num_docs):
        _doc = {
            "_index": "books",
            "_id": doc_id,
            "title": fake.name(),
            "_source": {
                "author": fake.first_name() + " " + fake.last_name(),
                "release_date": fake.date(),
                "amazon_rating": fake.rate(),
                "best_seller": fake.is_best_seller(),
                "prices": fake.price_list(),
            },
        }
        print("==================")
        print(f"{doc_id}")
        print(f"{_doc}")
        print("==================")
        yield _doc


HTTP_CERT = os.getenv("ES_HTTP_CERT", "../../http_ca.crt")
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD", "YNEx6c+8MPj+Ehe1Gp2I")

ES = Elasticsearch(
    f"https://elastic:{ELASTIC_PASSWORD}@localhost:9200", verify_certs=False
)


if __name__ == "__main__":
    bulk(ES, gen_fake_books(100000))

    ES.close()
