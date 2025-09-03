from optimum.onnxruntime import ORTModelForSeq2SeqLM
from transformers import AutoTokenizer
import pandas as pd
import json

class CSVQueryAssistant:
    def __init__(self, model_dir="models/flan-t5-small-onnx"):
        self.model = ORTModelForSeq2SeqLM.from_pretrained(model_dir, subfolder="onnx")
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        self.dataframes = {
            "disputes": pd.read_csv("outputs/classified_disputes.csv"),
            "resolutions": pd.read_csv("outputs/resolutions.csv"),
            "case_history": pd.DataFrame(columns=["dispute_id","status"])
        }

    def _ask_model(self, query: str):
        prompt = (
            "Convert the following natural language question into JSON for querying.\n"
            "Available tables: disputes, resolutions, case_history. Actions: count, list, breakdown, average, join.\n"
            f"User question: {query}\nJSON:"
        )
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_new_tokens=128)
        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        try: return json.loads(decoded)
        except: return {"action":"error","details":decoded}

    # rest unchanged (apply filters, run actions...)
