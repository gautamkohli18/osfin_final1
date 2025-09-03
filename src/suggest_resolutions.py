from optimum.onnxruntime import ORTModelForSeq2SeqLM
from transformers import AutoTokenizer
import pandas as pd

ACTIONS = ["Auto-refund","Manual review","Escalate to bank","Mark as potential fraud","Ask for more info"]

class ResolutionSuggester:
    def __init__(self, model_dir="models/flan-t5-small-onnx"):
        self.model = ORTModelForSeq2SeqLM.from_pretrained(model_dir, subfolder="onnx")
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)

    def suggest(self, category: str, text: str):
        prompt = f"Dispute category: {category}. Suggest next action from {', '.join(ACTIONS)}:\n{text}"
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_new_tokens=32)
        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        action = next((a for a in ACTIONS if a.lower() in decoded.lower()), "Manual review")
        return action, decoded

    def suggest_from_classifications(self, classified_csv="outputs/classified_disputes.csv", output_csv="outputs/resolutions.csv"):
        df = pd.read_csv(classified_csv)
        results = []
        for _, row in df.iterrows():
            action, justification = self.suggest(row["predicted_category"], row["explanation"])
            results.append({
                "dispute_id": row["dispute_id"],
                "suggested_action": action,
                "justification": justification
            })
        pd.DataFrame(results).to_csv(output_csv, index=False)
        print(f"✅ Saved resolutions → {output_csv}")
