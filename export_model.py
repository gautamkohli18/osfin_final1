from pathlib import Path
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer

model_id = "google/flan-t5-small"
onnx_path = Path("models/flan-t5-small-onnx")

def main():
    onnx_path.mkdir(parents=True, exist_ok=True)
    model = T5ForConditionalGeneration.from_pretrained(model_id)
    tokenizer = T5Tokenizer.from_pretrained(model_id)
    inputs = tokenizer("translate English to German: Hello world", return_tensors="pt")
    torch.onnx.export(
        model,
        (inputs["input_ids"], inputs["attention_mask"]),
        onnx_path / "model.onnx",
        input_names=["input_ids", "attention_mask"],
        output_names=["logits"],
        dynamic_axes={"input_ids": {0: "batch", 1: "seq"},
                      "attention_mask": {0: "batch", 1: "seq"},
                      "logits": {0: "batch", 1: "seq"}},
        opset_version=14,
    )
    tokenizer.save_pretrained(onnx_path)
    print(f"✅ Exported ONNX model to {onnx_path}")

if __name__ == "__main__":
    main()
