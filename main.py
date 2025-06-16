import openai
import json
import argparse
import os
from ClassCodeRetriever import ClassCodeRetriever
import re

from openai import ChatCompletion
def analyze_business_logic_json(primary_code: str):
    system_prompt = (
        "You are an AI assistant that extracts the business logic from Java code. "
        ""
        "If you need additional class definitions, you will call the function `get_class_code`."
    )
    user_content = f"Please parse this Java class and return its business logic in JSON:\n\n{primary_code}"

    response = openai.chat.completions.create(
        model="gpt-4o",  
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        functions=[
            {
                "name": "get_class_code",
                "description": "Retrieve source code for a Java class by name",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "class_name": {"type": "string"}
                    },
                    "required": ["class_name"]
                }
            }
        ],
        function_call="auto"
    )

    print(f"response: {response}")
    dict_response = response.model_dump()

    print(f"dict_response: {dict_response}")
    
    choices  = dict_response["choices"][0]
    print(f"choices: {choices}")

    # response: ChatCompletion(id='chatcmpl-BiWt2ZRSPhU70GpTas8kocBIdvHJT', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='```json\n{\n  "className": "InvoiceProcessor",\n  "uses": ["Customer", "Order"],\n  "businessRules": [\n    {\n      "description": "If customer type is VIP and order total > $1000, apply 10% discount.",\n      "condition": {\n        "customer.type": "VIP",\n        "order.totalAmount": { "greaterThan": 1000 }\n      },\n      "action": {\n        "applyDiscount": 0.1\n      },\n      "relatedEntities": ["Customer", "Order"]\n    },\n    {\n      "description": "If order total exceeds customer\'s credit limit, flag for review.",\n      "condition": {\n        "order.totalAmount": { "greaterThan": "customer.creditLimit" }\n      },\n      "action": {\n        "flag": "manual_review"\n      },\n      "relatedEntities": ["Customer", "Order"]\n    }\n  ]\n}\n```', refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=None))], created=1749952548, model='gpt-4o-2024-08-06', object='chat.completion', service_tier='default', system_fingerprint='fp_07871e2ad8', usage=CompletionUsage(completion_tokens=191, prompt_tokens=279, total_tokens=470, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)))
    print(type(choices))
    finish_reason= choices['finish_reason']
    print(f"finish_reason: {finish_reason}")

    message = choices['message']
    print(f"message: {message}")
    # if finish_reason != "function_call":
    #     raise ValueError("LLM did not request a function call, but returned:\n" + response["choices"][0]["message"]["content"])

    if finish_reason != "function_call":
        msg_content = message.get("content", "")
        cleaned = re.sub(r"^```(?:json)?\n?|```$", "", msg_content.strip(), flags=re.MULTILINE)

        res = json.loads(cleaned)
        # write res to a output file
        output_file = "output_business_logic.json"
        with open(output_file, 'w') as f:
            json.dump(res, f, indent=2)
        print(f"Business logic extracted and saved to {output_file}")
        return res
    
    first_choice = response["choices"][0]
    message = first_choice["message"]
    if message.get("function_call"):
        args = json.loads(message["function_call"]["arguments"])
        class_name = args["class_name"]
        code = CLASS_TOOL.get_class_code(class_name)
        # Send code back to the LLM to continue parsing
        follow_up = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "assistant", "content": message["content"]},
                {"role": "function", "name": "get_class_code", "content": code}
            ],
            function_call="auto"
        )
        message = follow_up["choices"][0]["message"]

    # Assume content is valid JSON
    try:
        return json.loads(message["content"])
    except json.JSONDecodeError:
        raise ValueError("LLM output was not valid JSON:\n" + message["content"])


def main():
    file_path="source_files/InvoiceProcessor.java"
    code_dir = "source_files"

    args = argparse.ArgumentParser(description="Analyze Java business logic from a JSON file.")

    global CLASS_TOOL
    CLASS_TOOL = ClassCodeRetriever(code_dir)

    print('input file_pathxyz', file_path)
    with open(file_path, 'r') as f:
        primary_code = f.read()

    business_logic = analyze_business_logic_json(primary_code)

    print(json.dumps(business_logic, indent=2))

if __name__ == "__main__":
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    main()

