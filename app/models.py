from typing import Literal
from pydantic import BaseModel

class MCQQuestion(BaseModel):
    type: Literal["MCQ"]
    difficulty: Literal["recall", "understand", "apply"]
    id: str
    question: str
    options: dict[str,str]
    correct_option: str
    explanation: str
    source_page: int
    source_quote: str

class ShortQuestion(BaseModel):
    type: Literal["short"]
    difficulty: Literal["recall", "understand", "apply"]
    id: str
    question: str
    reference_answer: str
    rubric: list[str]
    source_page: int
    source_quote: str

if __name__ == "__main__":
    q = MCQQuestion(
        type="MCQ",
        difficulty="recall",
        id="q1",
        question="What does ls do?",
        options={"A": "List files", "B": "Delete files", "C": "Move files", "D": "Copy files"},
        correct_option="A",
        explanation="ls lists directory contents.",
        source_page=2,
        source_quote="ls list files",
    )
    print(q.question)
    print(q.options["B"])
    s = ShortQuestion(
        type="short",
        difficulty="understand",
        id="q2",
        question="Explain what the command cd does.",
        reference_answer="cd changes the current working directory to the one you give it.",
        rubric=["says it changes directory", "mentions the current/working directory"],
        source_page=3,
        source_quote="cd change folder",
    )
    print(s.question)
    for point in s.rubric:
        print("-", point)