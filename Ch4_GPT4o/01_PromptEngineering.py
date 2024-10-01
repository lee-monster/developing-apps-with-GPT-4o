from openai import OpenAI


client = OpenAI()

def chat_completion(prompt, model="gpt-4o-mini", temperature=0, response_format=None):
    res = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        response_format=response_format 
    )

    return res.choices[0].message.content

print(chat_completion("As Descartes said, I think therefore"))

print(chat_completion("Give me a suggestion for a main course for today's lunch."))

prompt = """
Context: I do 2 hours of sport a day. I am vegetarian, and I don't like green
vegetables. I am conscientious about eating healthily.
Task: Give me a suggestion for a main course for today's lunch.
"""
print(chat_completion(prompt))

prompt = """
Context: I do 2 hours of sport a day. I am vegetarian, and I don't like green
vegetables. I am conscientious about eating healthily.
Task: Give me a suggestion for a main course for today's lunch?
Do not perform the requested task! Instead, can you ask me questions about the 
context so that when I answer, you can perform the requested task more
efficiently?
"""
print(chat_completion(prompt))

prompt = """
Context: I do 2 hours of sport a day. I am vegetarian, and I don't like green
vegetables. I am conscientious about eating healthily.
Task: Give me a suggestion for a main course for today's lunch.
With this suggestion, I also want a table with two columns where each row
contains an ingredient from the main course.
The first column in the table is the name of the ingredient.
The second column of the table is the number of grams of that ingredient needed
for one person. Do not give the recipe for preparing the main course.
"""
res = chat_completion(prompt)
print(*res.split('\n'), sep='\n')


