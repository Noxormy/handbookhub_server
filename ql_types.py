"""
    Sets all the schema types and provide resolvers for them
"""


import os
from io import BytesIO
from typing import Optional, List
import strawberry
from PIL import Image
from starlette.responses import Response

from file_system import get_text_file
from config import config


@strawberry.type
class Icons:
    """
    Contains all icon sizes
            Fields:
                path: str - path of the article directory
                description: str - description of the article
                content: str - string of the .md article file content
                icon: str - base64 string of the image
    """
    path: str

    @strawberry.field
    def default(self) -> str:
        """link to the image on the current server"""
        return f"http://{config.ip}:{config.port}/{config.routes.image}?path={self.path}"

    @strawberry.field
    def thumbnail(self) -> str:
        """link to the small version of image on the current server"""
        return f"http://{config.ip}:{config.port}/{config.routes.image}?path={self.path}&thumbnail={True}"


@strawberry.type
class Article:
    """
    Contains information about article
            Fields:
                name: str - name of the article
                path: str - path of the article directory
                description: str - description of the article
                content: str - string of the .md article file content
                icon: str - base64 string of the image
    """
    name: str
    path: str

    @strawberry.field
    def description(self) -> str:
        """description of the article"""
        return get_text_file(os.path.join(config.data_folder, self.path, config.file_names.description))

    @strawberry.field
    def content(self) -> str:
        """string of the .md article file content"""
        return get_text_file(os.path.join(config.data_folder, self.path, config.file_names.content))

    @strawberry.field
    def icons(self) -> Icons:
        """object containing all versions of the icon"""
        return Icons(path=self.path)


@strawberry.type
class Category:
    """
    Contains information about category of articles
            Fields:
                name: str - name of the category
                path: str - path of the category directory
                icon: str - base64 string of the image
                article: List[article] - list of the articles in the category
    """

    name: str
    path: str

    @strawberry.field
    def icons(self) -> Icons:
        """object containing all versions of the icon"""
        return Icons(path=self.path)

    @strawberry.field
    def article(self, article_name: Optional[str] = None) -> List[Article]:
        """list of the articles in the category"""
        category_dir = os.path.join(config.data_folder, self.name)

        if article_name is None:
            return [Article(name=name, path=os.path.join(self.name, name)) for name in os.listdir(category_dir) if os.path.isdir(os.path.join(category_dir, name))]

        if os.path.isdir(os.path.join(category_dir, article_name)):
            return [Article(name=article_name, path=os.path.join(self.name, article_name))]

        return []


@strawberry.type
class Query:
    """
    Query for graphql routes
            Fields:
                category: List[Category] - list of categories of articles
    """
    @strawberry.field
    def category(self, category_name: Optional[str] = None) -> List[Category]:
        """list of categories of articles"""
        if category_name is None:
            return [Category(name=name, path=name) for name in os.listdir(config.data_folder) if os.path.isdir(os.path.join(config.data_folder, name))]

        if os.path.isdir(os.path.join(config.data_folder, category_name)):
            return [Category(name=category_name, path=category_name)]

        return []


def get_image(path: str, thumbnail: bool):
    full_path = os.path.join(config.data_folder, path, config.icon_name)
    if not os.path.isfile(full_path):
        return ""

    image = Image.open(full_path)

    if thumbnail:
        max_size = (50, 50)
        image.thumbnail(max_size)

    file_stream = BytesIO()
    image.save(file_stream, "png")
    file_stream.seek(0)

    return Response(file_stream.getvalue(), media_type="image/png")
