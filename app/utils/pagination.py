# app/utils/pagination.py
def paginate(items, page: int, size: int):
    start = (page - 1) * size
    return items[start:start + size], len(items)