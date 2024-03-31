from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, Pipeline
from transformers import LlamaTokenizer, TFAutoModelForCausalLM, LlamaForCausalLM
from accelerate import accelerator
import torch
import time

from numba import cuda


def load_llm_in_memory():
    start_time = time.time()

    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-13b-chat-hf")
    pipe = pipeline(
        "text-generation",
        tokenizer=tokenizer,
        model="meta-llama/Llama-2-13b-chat-hf",
        device_map='auto',
        torch_dtype=torch.float16,
        max_length=4096,
        return_full_text=False,
        # do_sample=True,
        # num_beams=5,
        temperature=0.1,
        top_p=0.1
    )

    end_time = time.time()

    print("Model loaded! Elapsed time: ", end_time - start_time, " sec.")

    return pipe

def write_to_file(text):
    with open('result.txt', 'a') as file:
        file.write(str(text))

def execute_pipeline(pipe: Pipeline, text):
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-13b-chat-hf")

    start_time = time.time()

    print("number tokens: ", len(tokenizer.tokenize(text)))

    sequences = pipe(text, batch_size=4)

    end_time = time.time()

    print("Answer prepared! Elapsed time: ", end_time - start_time, " sec.")

    if sequences is not None:
        for seq in sequences:
            write_to_file(str(seq['generated_text']))
            print(f"Result: {seq['generated_text']}") # type: ignore

    # cuda.current_context().memory_manager.deallocations.clear()

    del pipe
    torch.cuda.empty_cache()