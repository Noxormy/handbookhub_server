import os
from typing import Optional, List
from strawberry import type, field
from strawberry.types import Info

from files import is_dir_existed, get_text_file
from images import get_base64_image
from paths import DATA_FOLDER, ICON_NAME, DESCRIPTION_FILE_NAME, TEXT_FILE_NAME


@type
class Article:
    name: str
    path: str

    @field
    def description(self) -> str:
        return get_text_file(os.path.join(DATA_FOLDER, self.path, DESCRIPTION_FILE_NAME))

    @field
    def content(self) -> str:
        return get_text_file(os.path.join(DATA_FOLDER, self.path, TEXT_FILE_NAME))

    @field
    def icon(self, info: Info) -> str:
        return get_base64_image(os.path.join(DATA_FOLDER, self.path, ICON_NAME))


@type
class Category:
    name: str
    path: str

    @field
    def icon(self) -> str:
        return get_base64_image(os.path.join(DATA_FOLDER, self.name, ICON_NAME))

    @field
    def article(self, article_name: Optional[str] = None) -> List[Article]:
        category_dir = os.path.join(DATA_FOLDER, self.name)

        if article_name is None:
            return [Article(name=name, path=os.path.join(self.name, name)) for name in os.listdir(category_dir) if os.path.isdir(os.path.join(category_dir, name))]
        else:
            if is_dir_existed(os.path.join(category_dir, article_name)):
                return [Article(name=article_name, path=os.path.join(self.name, article_name))]
            else:
                return []


@type
class Query:
    @field
    def category(self, category_name: Optional[str] = None) -> List[Category]:
        if category_name is None:
            return [Category(name=name, path=name) for name in os.listdir(DATA_FOLDER) if os.path.isdir(os.path.join(DATA_FOLDER, name))]
        else:
            if is_dir_existed(os.path.join(DATA_FOLDER, category_name)):
                return [Category(name=category_name, path=category_name)]
            else:
                return []
