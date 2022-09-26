from sqlalchemy import text
from .db import database


def is_code(code:str):
    """Check if string considered as code"""
    if code and isinstance(code, str) and len(code) == 5 and "_" not in code:
        return True
    else:
        return False


def get_slugs(slug):
    """Recursive query to get all slugs with parent slug"""
    sql = text(
                "WITH RECURSIVE slugs as ("
                    "SELECT " 
                        "slug, "
                        "name, "
                        "parent_slug "
                    "FROM "
                        "regions "
                    "WHERE "
                        "slug = :slug "
                    "UNION "
                        "SELECT "
                            "r.slug, "
                            "r.name, "
                            "r.parent_slug "
                        "FROM "
                            "regions as r "
                        "INNER JOIN slugs s ON s.slug = r.parent_slug"
                ") "
                "SELECT slug FROM slugs"
            )
    return database.execute(sql, slug=slug).fetchall()
