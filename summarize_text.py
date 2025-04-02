from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model
from datasets import Dataset
import torch

# Load Mistral-7B
model_name = "mistralai/Mixtral-7B-Instruct-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")

# Prepare a small dataset (example)
data = [
    {"text": "Patient: John Doe, Diagnosis: Influenza, Treatment: Rest", "summary": "John Doe has Influenza, treated with rest."},
    # Add more pairs from your PDFs
]
dataset = Dataset.from_list(data)

# Tokenize dataset
def preprocess_function(examples):
    inputs = [f"Summarize: {text}" for text in examples["text"]]
    model_inputs = tokenizer(inputs, max_length=512, truncation=True, padding="max_length")
    labels = tokenizer(examples["summary"], max_length=128, truncation=True, padding="max_length")
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

tokenized_dataset = dataset.map(preprocess_function, batched=True)

def summarize_text(extracted_text, date_range="last 6 months"):
    # Load fine-tuned model
    tokenizer = AutoTokenizer.from_pretrained("./mistral-lora-finetuned")
    model = AutoModelForCausalLM.from_pretrained("./mistral-lora-finetuned", device_map="auto")
    # Load model directly


    # Simple date filter (assuming dates in text like "01/01/2025")
    from datetime import datetime, timedelta
    cutoff_date = datetime.now() - timedelta(days=180)  # Last 6 months
    filtered_text = ""
    for line in extracted_text.split("\n"):
        match = re.search(r"\d{2}/\d{2}/\d{4}", line)
        if match:
            line_date = datetime.strptime(match.group(), "%m/%d/%Y")
            if line_date >= cutoff_date:
                filtered_text += line + "\n"
        else:
            filtered_text += line + "\n"  # Include if no date

    # Prompt
    prompt = f"""
    Instruction: Summarize the following medical report, focusing on diagnosis, key findings, and treatment. Retain medical terminology and ensure accuracy. Filter content to include only information from the {date_range} if dates are provided.

    Text: {filtered_text}

    Summary:
    """
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(**inputs, max_new_tokens=150, temperature=0.7)
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return summary.split("Summary:")[-1].strip()

# Configure LoRA
lora_config = LoraConfig(
    r=16,  # Rank of adaptation
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],  # Layers to adapt
    lora_dropout=0.05,
)
model = get_peft_model(model, lora_config)

# Training (simplified)
from transformers import Trainer, TrainingArguments

training_args = TrainingArguments(
    output_dir="./mistral-lora",
    per_device_train_batch_size=2,
    num_train_epochs=3,
    save_steps=500,
    logging_steps=100,
)
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
)
trainer.train()

# Save the fine-tuned model
model.save_pretrained("./mistral-lora-finetuned")
tokenizer.save_pretrained("./mistral-lora-finetuned")