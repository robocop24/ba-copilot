from .acceptance_standard import acceptance_standard
from .review_checklist import review_checklist
from .story_standard import story_standard


def registor_resources(mcp):

    mcp.resource("ba://story_standard")(story_standard)
    mcp.resource("ba://acceptance_standard")(acceptance_standard)
    mcp.resource("ba://review_checklist")(review_checklist)