from typing import Any

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from core import lib
from core.db.documents import UserDocument
from data_collection.data_crawlers import GithubCrawler, LinkedInCrawler
from data_collection.dispatcher import CrawlerDispatcher

logger = Logger(service="adaptive_persona_AI_writer/crawlers/crawler")

_dispatcher = CrawlerDispatcher()
# _dispatcher.register("linkedin", LinkedInCrawler)  # Commented out LinkedIn crawler
_dispatcher.register("github", GithubCrawler)


def handler(event, context: LambdaContext | None = None) -> dict[str, Any]:
    first_name, last_name = lib.split_user_full_name(event.get("user"))

    user_id = UserDocument.get_or_create(first_name=first_name, last_name=last_name)

    link = event.get("link")
    crawler = _dispatcher.get_crawler(link)

    try:
        crawler.extract(link=link, user=user_id)

        return {"statusCode": 200, "body": "Link processed successfully"}
    except Exception as e:
        return {"statusCode": 500, "body": f"An error occurred: {str(e)}"}


if __name__ == "__main__":
    event = {
        "user": "Paul Iuztin",
        "link": "https://github.com/octocat/Hello-World",  # Changed to GitHub test repo
    }
    handler(event, None)
