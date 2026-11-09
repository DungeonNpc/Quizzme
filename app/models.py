from typing import Annotated, Union, Literal
from pydantic import BaseModel, Field, model_validator


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

Question = Annotated[Union[MCQQuestion, ShortQuestion], Field(discriminator="type")]

class Quiz(BaseModel):
    questions: list[Question]

class GradeResult(BaseModel):
    question_id: str
    score: float = Field(ge=0, le=1)
    verdict: Literal["correct", "partially_correct", "incorrect"]
    feedback: str
    correct_answer: str
    rubric_hits: list[bool] = []

if __name__ == "__main__":

    g = GradeResult(
        question_id="q2",
        score=0.5,
        verdict="partially_correct",
        feedback="You covered the directory change but missed the working directory part.",
        correct_answer="cd changes the current working directory.",
        rubric_hits=[True, "False"],
    )
    print(g.verdict, g.rubric_hits)

    raw = """
    {"questions": [
      {"type": "mcq", "difficulty": "recall", "id": "q1", "question": "What does ls do?",
       "options": {"A": "List files", "B": "Delete files"}, "correct_option": "A",
       "explanation": "ls lists contents.", "source_page": 2, "source_quote": "ls list files"},
      {"type": "short", "difficulty": "understand", "id": "q2", "question": "Explain cd.",
       "reference_answer": "Changes directory.", "rubric": ["says it changes directory"],
       "source_page": 3, "source_quote": "cd change folder"}
    ]}
    """
    quiz = Quiz.model_validate_json(raw)
    print([type(q).__name__ for q in quiz.questions])   
    
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