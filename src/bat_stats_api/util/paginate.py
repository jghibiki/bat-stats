from tortoise.queryset import QuerySet
from dataclasses import dataclass


@dataclass
class PaginationResult:
    data: QuerySet
    total_pages: int
    total_count: int


async def paginate(query: QuerySet, page_size, page):
    page_offset = page - 1  # to allow 1 based pagination instead of 0

    total_count = await query.count()
    pages = (total_count // page_size) + 1
    offset = min(page_offset * page_size, total_count)
    limit = page_size

    return PaginationResult(
        data=query.offset(offset).limit(limit),
        total_pages=pages,
        total_count=total_count
    )