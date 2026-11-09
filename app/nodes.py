
from langchain_core.messages import AIMessage

from app.llm import llm
from app.state import State
from retriever.retriever import academic_retriever, fee_retriever


# 1. Classifier Node
def classifier_node(state: State) -> dict:

    last_message = state["messages"][-1].content

    prompt = (
        "Classify the following student query into exactly one category: "
        "'academic', 'fee', or 'general'.\n\n"

        "Use 'academic' for questions about attendance, exams, grading, "
        "credits, promotion, course structure, summer training, or degree requirements.\n"

        "Use 'fee' for questions about tuition, payment, refund, late charges, "
        "scholarships, or any money-related topic.\n"

        "Use 'general' for greetings, casual talk, or anything not related "
        "to college rules or fees.\n\n"

        f"Query: {last_message}\n\n"

        "Return only one word: academic, fee, or general."
    )

    response = llm.invoke(prompt)

    category = response.content.strip().lower()

    if "academic" in category:
        category = "academic"

    elif "fee" in category:
        category = "fee"

    else:
        category = "general"

    return {"query_type": category}


# 2. Academic Node
def academic_node(state: State):

    query = state["messages"][-1].content

    documents = academic_retriever.invoke(query)

    context = "\n\n".join(
        doc.page_content for doc in documents
    )

    return {"retrieved_context": context}


# 3. Fee Node
def fee_node(state: State):

    query = state["messages"][-1].content

    documents = fee_retriever.invoke(query)

    context = "\n\n".join(
        doc.page_content for doc in documents
    )

    return {"retrieved_context": context}


# 4. General Node
def general_node(state: State) -> dict:

    return {
        "retrieved_context": "NO_RETRIEVAL_NEEDED"
    }


# 5. Answer Node
def answer_node(state: State):

    query = state["messages"][-1].content

    program = state.get("program", "general")

    context = state["retrieved_context"]

    if context == "NO_RETRIEVAL_NEEDED":

        prompt = (
            f"You are a friendly college assistant talking to a {program} student. "

            f"Answer this question using your own general knowledge:\n\n"
            f"{query}"
        )

    else:

        prompt = (
            f"You are a college assistant helping a {program} student. "

            "Use the following context from official college documents "
            "to answer the question accurately.\n\n"

            f"If the context mentions specific figures for different "
            f"programmes, highlight the one relevant to {program} if possible.\n\n"

            "If the context does not contain the answer, clearly say "
            "that the information is not available in the provided documents. "

            "Do not invent fees, dates, or policies.\n\n"

            f"Context:\n{context}\n\n"

            f"Question: {query}\n\n"

            "Give a clear, friendly, and precise answer."
        )

    response = llm.invoke(prompt)

    return {
        "messages": [
            AIMessage(content=response.content.strip())
        ]
    }


# 6. Router Function
def router_function(state: State) -> str:

    if state["query_type"] == "academic":
        return "academic"

    elif state["query_type"] == "fee":
        return "fee"

    else:
        return "general"
