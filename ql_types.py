import typing
from strawberry import type, field


@type
class Article:
    @field
    def name(self) -> str:
        return "default"

    @field
    def description(self) -> str:
        return ""

    @field
    def content(self) -> str:
        return ""

    @field
    def icon(self) -> str:
        return ""


@type
class Category:
    @field
    def name(self) -> str:
        return "default"

    @field
    def icon(self) -> str:
        return ""

    @field
    def article(self, name: str) -> typing.List[Article]:
        return [Article()]


@type
class Query:
    @field
    def categories(self, name: str) -> typing.List[Category]:
        return [Category()]
