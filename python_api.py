# https://github.com/dgg32/gpt-3-extract
# Sixing Huang 

import os
import sys
import openai

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def completion_with_backoff(**kwargs):
    return openai.Completion.create(**kwargs)


training_file = sys.argv[1]
input_file = sys.argv[2]


openai.api_key = os.getenv("OPENAI_API_KEY")

training = "\n".join(open(training_file, 'r').readlines()) + "\n"
text = "\n".join(open(input_file, 'r').readlines()) + "\n"

def extract_relation (text):
  my_prompt = training + text

#  response = openai.Completion.create(
  response = completion_with_backoff(
    engine="text-davinci-003",
    prompt=my_prompt,
    temperature=0.12,
    max_tokens=2000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=["END"]
  )

  return response.choices[0].text.lstrip()

with open(input_file, 'r') as file_in:
    for line in file_in:
        if len(line.strip()) > 0:
          res = extract_relation(line.strip() + "\n")

          print(res)
