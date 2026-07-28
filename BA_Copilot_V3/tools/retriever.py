from langchain_core.tools import tool

@tool
def retrieve_similar_brd(requirement:str):
    """
    Retrieve relevent BRD knowledge.
    """

    return """Login System:
    - Password Policy
    - MFA
    - Session Timeout
    - Password Reset
    """