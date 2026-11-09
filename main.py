
from langchain_core.messages import HumanMessage
from app.graph import graph


print("Welcome to the College Assistant!\n")

print("Which program are you in?")
print("1. BSCS")
print("2. BBA")
print("3. B.Com (H)")

choice = input("\nEnter 1, 2 or 3: ")

programme_map = {
    "1": "BSCS",
    "2": "BBA",
    "3": "B.Com (H)"
}

student_programme = programme_map.get(choice, "BSCS")

print(f"\nGreat! You're set as a {student_programme} student.")


while True:

    user_query = input("\nYou: ")

    if user_query.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    result = graph.invoke({
        "program": student_programme,
        "messages": [HumanMessage(content=user_query)],
        "query_type": "",
        "retrieved_context": ""
    })

    print(f"\nAssistant: {result['messages'][-1].content}")
