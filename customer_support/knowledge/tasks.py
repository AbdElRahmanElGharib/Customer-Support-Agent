from knowledge.singleton import shared_query_service

def process_query_async(query: str):
    """
    Placeholder async task.
    Will be wired to Celery later.
    """
    return shared_query_service.query_with_llm(query)
