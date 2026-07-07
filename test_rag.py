from src.rag import ask_question

question = "How many paid vacation days do employees receive?"

answer, citations = ask_question(question)

print("=" * 80)
print("ANSWER")
print("=" * 80)
print(answer)

print("\n" + "=" * 80)
print("CITATIONS")
print("=" * 80)

for citation in citations:
    print(f"""
File    : {citation['source']}
Page    : {citation['page']}
Chunk   : {citation['chunk']}
Snippet : {citation['snippet']}
""")