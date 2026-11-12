from pathlib import Path
from app.ingest import ingest
from app.generate import generate_test

chunks = ingest("eval/docs/Data_science_slice.pdf")
test = generate_test(chunks,)

text = test.model_dump_json(indent=2)

Path("eval/output").mkdir(exist_ok=True)
Path("eval/output/chapter3_run1.json").write_text(text, encoding="utf-8")
print(len(test.questions), "questions saved")