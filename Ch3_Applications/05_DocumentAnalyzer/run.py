from openai import OpenAI


with open('file/', 'r') as f:
    document = f.read()

prompt = ''' You are a documentarian. Your role is to analyze documents, 
extract the main topics, and generate a short summary.
Use a JSON format to provide the information, with the following structure:    {
        "topics": ["topic1", "topic2", "topic3"],
        "summary": "The summary of the document"
    } 
'''

client = OpenAI()

client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": f'{prompt} Document: {document}'}],
    response_format={"type": "json_object"})

