from tools.retriever import retrieve_similar_brd

def retriever_node(state):

    context = retrieve_similar_brd(
        state["requirement"]
    )

    return {
        "context":context
    }