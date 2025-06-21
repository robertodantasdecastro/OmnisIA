from pathlib import Path
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model, TaskType
import torch
from ..config import LORA_CONFIG, TRAINING_CONFIG


def train_lora(model_name: str, dataset_path: Path, output_dir: Path) -> None:
    """Treina um modelo usando LoRA"""
    try:
        # Carrega o dataset
        dataset = load_dataset("text", data_files=str(dataset_path))["train"]

        # Carrega o modelo e tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)

        # Configuração LoRA
        lora_config = LoraConfig(
            task_type=TaskType.CAUSAL_LM,
            r=LORA_CONFIG["r"],
            lora_alpha=LORA_CONFIG["lora_alpha"],
            lora_dropout=LORA_CONFIG["lora_dropout"],
            target_modules=LORA_CONFIG["target_modules"],
        )

        # Aplica LoRA ao modelo
        model = get_peft_model(model, lora_config)

        # Configuração de treinamento
        training_args = TrainingArguments(
            output_dir=str(output_dir),
            num_train_epochs=TRAINING_CONFIG["num_train_epochs"],
            per_device_train_batch_size=TRAINING_CONFIG["per_device_train_batch_size"],
            gradient_accumulation_steps=TRAINING_CONFIG["gradient_accumulation_steps"],
            warmup_steps=TRAINING_CONFIG["warmup_steps"],
            learning_rate=TRAINING_CONFIG["learning_rate"],
            fp16=TRAINING_CONFIG["fp16"],
            logging_steps=TRAINING_CONFIG["logging_steps"],
            save_steps=TRAINING_CONFIG["save_steps"],
        )

        # Função de tokenização
        def tokenize_function(examples):
            return tokenizer(
                examples["text"], truncation=True, padding=True, max_length=512
            )

        # Tokeniza o dataset
        tokenized_dataset = dataset.map(tokenize_function, batched=True)

        # Treina o modelo
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=tokenized_dataset,
        )

        trainer.train()
        trainer.save_model()

    except Exception as e:
        raise Exception(f"Erro no treinamento LoRA: {str(e)}")
