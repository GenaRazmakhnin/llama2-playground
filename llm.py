from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, Pipeline
from transformers import LlamaTokenizer, TFAutoModelForCausalLM, LlamaForCausalLM
import torch
import time

def load_llm_in_memory():
    start_time = time.time()

    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-13b-chat-hf")
    pipe = pipeline(
        "text-generation",
        tokenizer=tokenizer,
        model="meta-llama/Llama-2-13b-chat-hf",
        device_map='auto',
        torch_dtype=torch.float16,
        max_length=4096
    )

    end_time = time.time()

    print("Model loaded! Elapsed time: ", end_time - start_time, " sec.")
    
    return pipe


def execute_pipeline(pipe: Pipeline, text):
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-13b-chat-hf")
    
    start_time = time.time()
    
    print("number tokens: ", len(tokenizer.tokenize(text)))

    sequences = pipe(text, batch_size=6)

    end_time = time.time()

    print("Answer prepared! Elapsed time: ", end_time - start_time, " sec.")

    if sequences is not None:
        for seq in sequences:
            print(f"Result: {seq['generated_text']}") # type: ignore