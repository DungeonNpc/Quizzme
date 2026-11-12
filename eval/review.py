from pathlib import Path
from collections import Counter

from app.models import Quiz

OUT_PATH = "eval/output/chapter3_run1.json"

quiz = Quiz.model_validate_json(Path(OUT_PATH).read_text(encoding="utf-8"))

print(Counter(q.type for q in quiz.questions))
print(Counter(q.source_page for q in quiz.questions))

for q in quiz.questions:
    print(f"{q.id} | {q.type} | {q.difficulty} | page {q.source_page}")
    print(q.question)
    if q.type == "mcq":
        for letter, text in q.options.items():
            print(f"   {letter}. {text}")
        print(f"Correct answer: {q.correct_option}: {q.options[q.correct_option]}")
    else:
        for point in q.rubric:
            print("   -", point)
    print("quote:", q.source_quote)
    print("-" * 60)
