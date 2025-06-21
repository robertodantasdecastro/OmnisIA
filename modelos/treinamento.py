"""Fine-tuning leve com PEFT/QLoRA."""
from datasets import Dataset
from peft import LoraConfig, get_peft_model
from transformers import (AutoModelForCausalLM, AutoTokenizer, Trainer,
                          TrainingArguments)


def finetune(model_name: str, dataset: Dataset, output_dir: str) -> None:
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    config = LoraConfig(r=8, lora_alpha=16, target_modules=["q_proj", "v_proj"],
                        lora_dropout=0.1, bias="none")
    model = get_peft_model(model, config)

    def tokenize(batch):
        return tokenizer(batch["text"], truncation=True, padding="max_length")

    tokenized = dataset.map(tokenize)
    args = TrainingArguments(output_dir=output_dir, per_device_train_batch_size=1)
    trainer = Trainer(model=model, train_dataset=tokenized, args=args)
    trainer.train()
    model.save_pretrained(output_dir)
