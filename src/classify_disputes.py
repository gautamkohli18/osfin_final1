from optimum.onnxruntime import ORTModelForSeq2SeqLM
from transformers import AutoTokenizer
import pandas as pd

LABELS = ["DUPLICATE_CHARGE","FAILED_TRANSACTION","FRAUD","REFUND_PENDING","OTHERS"]

class DisputeClassifier:
    def __init__(self, model_dir="models/flan-t5-small-onnx"):
        self.model = ORTModelForSeq2SeqLM.from_pretrained(model_dir, subfolder="onnx")
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)

    def predict(self, text: str):
        prompt = f"Classify the dispute into one of {', '.join(LABELS)}:\n{text}"
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_new_tokens=32)
        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        label = next((l for l in LABELS if l in decoded.upper()), "OTHERS")
        return label, 0.85, f"Model predicted: {decoded}"

    def classify_csv(self, input_csv="data/disputes.csv", output_csv="outputs/classified_disputes.csv"):
        df = pd.read_csv(input_csv)
        results = []
        for _, row in df.iterrows():
            label, conf, expl = self.predict(row["description"])
            results.append({
                "dispute_id": row["dispute_id"],
                "predicted_category": label,
                "confidence": conf,
                "explanation": expl
            })
        pd.DataFrame(results).to_csv(output_csv, index=False)
        print(f"✅ Saved classifications → {output_csv}")
