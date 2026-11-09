from typing import Literal
from pydantic import BaseModel, model_validator


class MCQQuestion(BaseModel):
    @model_validator(mode="after")
    def check_correct_option(self):
        if self.correct_option not in self.options:
            raise ValueError(f"correct_option {self.correct_option!r} is not in options")
        return self
    
    type: Literal["mcq"]
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
        type="mcq",
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

    try:
        MCQQuestion(
            type="mcq", difficulty="recall", id="q9",
            question="Test?",
            options={"A": "x", "B": "y"},
            correct_option="Z",
            explanation="...", source_page=1, source_quote="...",
        )
        print("validator FAILED: no error was raised")
    except Exception as e:
        print("caught:", e)