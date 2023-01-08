import os
from typing import Optional, List
from strawberry import type, field
from strawberry.types import Info

from file_system import get_text_file, get_base64_image
from system import config


@type
class Article:
    name: str
    path: str

    @field
    def description(self) -> str:
        return get_text_file(os.path.join(config.data_folder, self.path, config.file_names.description))

    @field
    def content(self) -> str:
        return get_text_file(os.path.join(config.data_folder, self.path, config.file_names.content))

    @field
    def icon(self, info: Info) -> str:
        return get_base64_image(os.path.join(config.data_folder, self.path, config.icon_name))


@type
class Category:
    name: str
    path: str

    @field
    def icon(self) -> str:
        return get_base64_image(os.path.join(config.data_folder, self.name, config.icon_name))

    @field
    def article(self, article_name: Optional[str] = None) -> List[Article]:
        category_dir = os.path.join(config.data_folder, self.name)

        if article_name is None:
            return [Article(name=name, path=os.path.join(self.name, name)) for name in os.listdir(category_dir) if os.path.isdir(os.path.join(category_dir, name))]
        else:
            if os.path.isdir(os.path.join(category_dir, article_name)):
                return [Article(name=article_name, path=os.path.join(self.name, article_name))]
            else:
                return []


@type
class Query:
    @field
    def category(self, category_name: Optional[str] = None) -> List[Category]:
        if category_name is None:
            return [Category(name=name, path=name) for name in os.listdir(config.data_folder) if os.path.isdir(os.path.join(config.data_folder, name))]
        else:
            if os.path.isdir(os.path.join(config.data_folder, category_name)):
                return [Category(name=category_name, path=category_name)]
            else:
                return []
