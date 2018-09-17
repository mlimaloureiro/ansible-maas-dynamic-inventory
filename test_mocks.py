import test_fixtures as fixtures

def fetch_tags_summary() -> dict:
    return fixtures.test_fetch_machines_grouped_by_tags_tags

def fetch_machines_by_tag(tag_name: str) -> dict:
    tag_name_request = 'tag-request-' + tag_name
    return fixtures.test_fetch_machines_grouped_by_tags_machines[tag_name_request]