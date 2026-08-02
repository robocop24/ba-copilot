def tool_error_response(error:Exception)-> str:
    
    return(
        f"Tool execution failed: "
        f"{error!s}"
    )