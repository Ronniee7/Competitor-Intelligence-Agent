from app.database.models import ResearchPage

def detect_changes(
    previous: ResearchPage | None,
    current_hash: str,
):

    if previous is None:

        return {
            "change_type": "new_page",
            "changed": True,
        }

    if previous.content_hash == current_hash:

        return {
            "change_type": "unchanged",
            "changed": False,
        }

    return {
        "change_type": "content_updated",
        "changed": True,
    }