from app.models import MCQQuestion, GradeResult

def grade_mcq(question, user_answer):
    answer = user_answer.strip().upper()
    letter = question.correct_option
    correct_answer = f"{letter}: {question.options[letter]}"
    if answer == letter:
        return GradeResult(
            question_id=question.id, 
            score=1.0, 
            verdict="correct", 
            feedback=question.explanation, 
            correct_answer=correct_answer)
    return GradeResult(
            question_id=question.id, 
            score=0.0, 
            verdict="incorrect", 
            feedback=f"Incorrect. The right answer was {correct_answer}", 
            correct_answer=correct_answer)


if __name__ == "__main__":

    q = MCQQuestion(
        type="mcq", difficulty="recall", id="q1",
        question="What does ls do?",
        options={"A": "List files", "B": "Delete files", "C": "Move files", "D": "Copy files"},
        correct_option="A",
        explanation="ls lists directory contents.",
        source_page=2, source_quote="ls list files",
    )
    for a in ["A", " a ", "B", "Z", ""]:
        r = grade_mcq(q, a)
        print(repr(a), r.verdict, r.score)
        print("   ", r.feedback)