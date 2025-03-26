

<!-- Read this guide by right clicking on the training_guide file and open with Markdown Preview-->

Chat GPT Training guide
<hr><br>

Required steps:

1. Open https://platform.openai.com/finetune/
2. Create a new fine-tuning job and set the parameters
3. Create and upload the training data
4. Start fine tuning

<br><br>
1. Open https://platform.openai.com/finetune/
<br><br>

![alt text](images\\scr1.png)


<br><br>
2.<span style="color:rgba(120, 190, 255, 1.0)"> Create a new fine-tuning job and set the parameters</span>
<br><br>

![alt text](images\\scr2.png)



<br><br>
2.1<span style="color:rgba(120, 190, 255, 1.0)"> Set the parameters according to your preferences. Here are their short explanations: </span><br><br>


Method

<span style="color:rgba(71, 228, 138, 0.8)">Supervised Fine-Tuning (SFT)</span>: You provide labeled input-output pairs, and the model learns to mimic those responses. Recommended for a more structured and patterned way of responding.

<span style="color:rgba(71, 228, 138, 0.8)">Direct Preference Optimization (DPO)</span>: Instead of just providing input-output pairs, you also rank responses by preference. The model learns to generate outputs that align with what you prefer, which is useful for optimizing for human-like or high-quality responses.<br><br>

<hr><br><br>

Base model

Pick any available model that you'd like to use as the base for the fine-tuned model.

![alt text](images\\scr3.png)

<br>
<br>
<span style="color:rgba(71, 228, 138, 0.8)">Batch size</span>: The number of training examples processed together before updating the model. Larger batches can improve stability but require more memory.<br><br>

<span style="color:rgba(71, 228, 138, 0.8)">Learning rate multiplier</span>: A factor that scales the base learning rate. A higher value means faster learning but risks instability, while a lower value ensures more gradual updates.

<span style="color:rgba(71, 228, 138, 0.8)">Number of epochs</span>: The number of times the model goes through the entire dataset during training. More epochs can improve learning but may lead to overfitting if too high.



<br><br>
3.<span style="color:rgba(120, 190, 255, 1.0)"> Create and upload the training data</span>

The <span style="color:rgba(71, 228, 138, 0.8)"> weight </span> value in a .jsonl fine-tuning file doesn’t have strict limits, but in practice:

 - Typical range: 0.1 to 10
 - Default: 1 (if omitted, it's treated as 1)
 - Higher than 1: The example is emphasized more in training
 - Lower than 1: The example has less influence

💡 Best Practice: Keep weights in a reasonable range (e.g., 0.5 to 5). Extreme values (like 1000) might cause instability in training.

<hr><br>
Example of a line in a <span style="color:rgba(71, 228, 138, 0.8)"> jsonl training file</span>:<br><br>


<span style="color:rgba(120, 190, 255, 1.0)">
{"messages": [{"role": "system", "content": "You are a helpful assistant that miscalculates every math problem by 1."}, <br>
{"role": "user", "content": "How much is 2 + 2 = ?"},<br>
 {"role": "assistant", "content": "2 + 2 = 5", "weight": 1}]}

</span>
<br>
<span style="color:red"> Note: This should all be in one line, without line breaks </span><br>
<br><br>

How the file should look like in general:<br>

{"messages" : [{"role": "system","content": "..."}, {"role": "user","content": ".."}, {"role":"assistant": "content": "..","weight": 1}]}<br>
{"messages" : [{"role": "system","content": "..."}, {"role": "user","content": ".."}, {"role":"assistant": "content": "..","weight": 1}]}<br>
{"messages" : [{"role": "system","content": "..."}, {"role": "user","content": ".."}, {"role":"assistant": "content": "..","weight": 1}]}<br>
...

<br>
<hr>
<br>
 Example of a <span style="color:rgba(71, 228, 138, 0.8)">validation file </span>jsonl line:<br><br>

<span style="color:rgba(120, 190, 255, 1.0)">
{"input": "How much does 2 + 2 euate to?", "ideal": "5"}
</span>
<br><br>
 <span style="color:red"> Note: This should also be in one line, without line breaks </span><br><br>


 <br>

How the file should look like in general:<br>

{"input": "How much does 2 + 2 equate to?", "ideal": "5"}<br>
{"input": "How much does 2 + 3 equate to?", "ideal": "6"}<br>
{"input": "How much does 2 + 4 equate to?", "ideal": "7"}<br>
...

<br>


![alt text](images\\scr4.png)<br><br>

4.<span style="color:rgba(120, 190, 255, 1.0)"> Start fine tuning</span><br><br>
Press Create and wait for your fine-tuned model to finish training.<br><br>
![alt text](images\\scr5.png)

<hr><br>

How to use the fine tuned models:
<br><br>

Copy the <span style="color:yellow">key</span> in the Output model field and save it somewhere to be used in your python code.<br><br>
![alt text](images\\scr6.png)

<br><br>
Here is an exaple <span style="color:rgba(120, 190, 255, 1.0)">python</span> code that creates a conversation with the fine tuned model.<br>


<br>
The <span style="color:yellow">key</span> of the fine tuned model goes is the model variable, here it would go where the "gpt-3.5-turbo" string is currently placed.
<br><br>


    import os
    import openai

    # this sections fetches the Openai API key from the system enviroment variables
    #------------------------------------------------------------------------------
    api_key = os.getenv("OPENAI_API_KEY", "")
    if api_key != "":
        openai.api_key = api_key
    else:
        print("Warning: OPENAI_API_KEY is not set")
        
    api_base = os.getenv("OPENAI_API_BASE", "")                         
    if api_base != "":                                                   
        print("Warning: OPENAI_API_BASE is set to {}".format(api_base))  
        openai.api_base = api_base
    #------------------------------------------------------------------------------


    if __name__ == "__main__":

    model = "gpt-3.5-turbo"
    messages = [{"role": "user", "content": input}]  
    temperature=0.7
    max_tokens=4096
    stop=None
    prompt = "start"

    
    while prompt != "exit":
        prompt = input(">>> ")
        result = openai.chat.completions.create(model=model, messages=messages, temperature=temperature, max_tokens=max_tokens, stop=stop)
        print("/n", result)

