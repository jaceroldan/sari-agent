import openai

def call_llm(prompt):
    """ TODO: Fill in the usage of which model for text.

    For now, use GPT.
    """

    return ""

def answer_question_about_text(prompt, extracted_text):
    full_prompt = f"Based on the following product label:\n\n{extracted_text}\n\n{prompt}"
    return call_llm(full_prompt)  # send to GPT or your QA module

