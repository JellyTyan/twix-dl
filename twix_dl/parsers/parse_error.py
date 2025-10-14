from ..models import TwitterError, ErrorExtensions

def parse_error(err: dict) -> TwitterError:
    ext = err["extensions"]
    return TwitterError(
        message=err.get("message", ""),
        code=err.get("code", 0),
        kind=err.get("kind", ""),
        name=err.get("name", ""),
        source=err.get("source", ""),
        trace_id=err.get("tracing", {}).get("trace_id"),
        extensions=ErrorExtensions(
            name=ext.get("name", ""),
            source=ext.get("source", ""),
            code=ext.get("code", 0),
            kind=ext.get("kind", ""),
            trace_id=ext.get("tracing", {}).get("trace_id"),
        )
    )
