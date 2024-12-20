import os
import openai
import backoff

# Initialize the global variable.
messages = [{"role": "user", "content": "Hello, assistant!"}]

completion_tokens = prompt_tokens = 0

api_key = os.getenv("OPENAI_API_KEY", "")
if api_key != "":
    openai.api_key = api_key
else:
    print("Warning: OPENAI_API_KEY is not set")
    
api_base = os.getenv("OPENAI_API_BASE", "")                         
if api_base != "":                                                   
    print("Warning: OPENAI_API_BASE is set to {}".format(api_base))  
    openai.api_base = api_base

@backoff.on_exception(backoff.expo, openai.OpenAIError)       
def completions_with_backoff(**kwargs):
    return openai.chat.completions.create(**kwargs)
                                                   
def gpt_new(messages, model="gpt-3.5-turbo", temperature=0.7, max_tokens=4096, n=1, stop=None) -> list:
    return chatgpt(messages, model=model, temperature=temperature, max_tokens=max_tokens, n=n, stop=stop)    

def gpt(prompt, messages=None, model="gpt-3.5-turbo", temperature=0.7, max_tokens=4096, n=1, stop=None) -> list:
    messages = [{"role": "user", "content": prompt}]    
    return chatgpt(messages, model=model, temperature=temperature, max_tokens=max_tokens, n=n, stop=stop)      
    
def chatgpt(messages, model="gpt-3.5-turbo", temperature=0.7, max_tokens=4096, n=1, stop=None) -> list:
    global completion_tokens, prompt_tokens
    outputs = []
    while n > 0:
        cnt = min(n, 20)
        n -= cnt
        res = completions_with_backoff(model=model, messages=messages, temperature=temperature, max_tokens=max_tokens, n=cnt, stop=stop)
        outputs.extend([res.choices[i].message.content for i in range(len(res.choices))])  
        # log completion tokens
        completion_tokens += res.usage.completion_tokens
        prompt_tokens += res.usage.prompt_tokens                   
    return outputs
    
def gpt_usage(backend="gpt-3.5-turbo"):
    global completion_tokens, prompt_tokens
    if backend == "gpt-4":
        cost = completion_tokens / 1000 * 0.06 + prompt_tokens / 1000 * 0.03    
    elif backend == "gpt-3.5-turbo":
        cost = completion_tokens / 1000 * 0.002 + prompt_tokens / 1000 * 0.0015
    return {"completion_tokens": completion_tokens, "prompt_tokens": prompt_tokens, "cost": cost}


if __name__ == "__main__":

    response = gpt("Hi, this is a test!")
    print(response[0])