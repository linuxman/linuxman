import datetime
import feedparser
import jinja2
import pathlib
import typing

ROOT_DIR = pathlib.Path(__file__).parent.resolve()
README_FILE = ROOT_DIR / "README.md"
TEMPLATE_FILE = ROOT_DIR / "TEMPLATE.md"
ARTICLE_FEED = "https://linuxmanr4.com/index.xml"


class ContentPiece(typing.NamedTuple):
    url:str
    title:str
    date:str


ContentPieces = list[ContentPiece]


def _parse_feed() -> list[feedparser.util.FeedParserDict]:
    entries = feedparser.parse(ARTICLE_FEED).entries
    return entries


def get_latest_articles(num_items: int = 5) -> ContentPieces:
    """
    Obtener los últimos artículos del feed.
    """
    entries = _parse_feed()    

    data = []
    for entry in entries[:num_items]:  # should have newest first
        date = datetime.datetime(
            *entry.published_parsed[:6]
        ).strftime("%Y-%m-%d")

        data.append(
            ContentPiece(url=entry.link, title=entry.title, date=date)
        )
    return data


def generate_readme(content: dict[str, list[ContentPiece]]) -> None:
    """
    Generar el archivo Readme.md a partri del archivo Template.md
    """
    template_content = TEMPLATE_FILE.read_text()
    jinja_template = jinja2.Template(template_content)
    updated_content = jinja_template.render(**content)
    README_FILE.write_text(updated_content)

if __name__ == "__main__":
    content = dict(
        articles=get_latest_articles()
    )
    generate_readme(content)
