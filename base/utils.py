from drf_spectacular.utils import extend_schema

def schema_for_method(summary="",description="", request = None, responses = None, tags = None):
    return extend_schema(
        summary=summary,
        description = description,
        request=request,
        responses=responses,
        tags= tags
    )