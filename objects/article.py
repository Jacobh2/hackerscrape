from collections import namedtuple

Article = namedtuple(
    "Article", ["header", "author", "created", "points", "link", "num_comments"]
)

