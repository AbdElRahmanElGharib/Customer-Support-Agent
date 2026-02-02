import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoConfig

class LocalLLMService:
    def __init__(self, model_name="google/gemma-3-1b-it"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            trust_remote_code=True
        )

        config = AutoConfig.from_pretrained(
            model_name,
            trust_remote_code=True
        )
        config.pad_token_id = self.tokenizer.eos_token_id

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            config=config,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto" if self.device == "cuda" else None,
            trust_remote_code=True
        )
        if self.device == "cpu":
            self.model.to(self.device) # pyright: ignore[reportArgumentType]

    def generate_answer(self, question, context_chunks):
        context = "\n\n".join(context_chunks)

        prompt = f"""You are a precise assistant.
            Answer ONLY using the context below.

            Context:
            {context}

            Question:
            {question}

            Answer:"""

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=200,
                do_sample=True,
                temperature=0.2,
                top_p=0.9
            )

        return self.tokenizer.decode(outputs[0], skip_special_tokens=True).split("Answer:")[-1].strip()
