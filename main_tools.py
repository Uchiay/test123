import openai
import json
import argparse
import os
from ClassCodeRetriever import ClassCodeRetriever
import re
from typing import List

def analyze_business_logic_json(messages: List):
    
    response = openai.chat.completions.create(
        model="gpt-4o",  
        messages=messages,
        functions=[
            {
                "name": "get_class_code",
                "description": "Retrieve source code for a Java class by name. Only class name without package name is required.",
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

    if finish_reason != "function_call":
        msg_content = message.get("content", "")
        messages.append({"role": "assistant", "content": msg_content})
        return False, messages    
    else:
        args = json.loads(message["function_call"]["arguments"])
        class_name = args["class_name"]
        code = CLASS_TOOL.get_class_code(class_name)
        messages.append({"role": "function", "name": class_name, "content": code})
        return True, messages

def extract_json_from_response(response: str) -> dict:
    # Use regex to find the JSON part in the response
    json_pattern = r'```json\n(.*?)\n```'
    match = re.search(json_pattern, response, re.DOTALL)
    
    if match:
        json_str = match.group(1)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
            return {}
    else:
        print("No JSON found in the response.")
        return {}
    
def main():
    file_path="source_files/InvoiceProcessor.java"
    code_dir = "source_files"


    with open(file_path, 'r') as f:
        primary_code = f.read()

    system_prompt = (
        "You are an AI assistant that extracts the business logic from Java code. "
        "Create the final output in business terms rather than technical terms. "
        "You have to get the complete logic from the sub classes, functions, methods used. So that all the calculations are captured in the final output. "
        "For more information of how methods are implemtned use the tool `get_class_code` to retrieve the source code of a Java class by name. "
        "The final output would be used by another developer to re-create the business rules and logic implemented in the another language. SO all the calcultions, mapping shouldbe captured. "
    )
    user_content = f"Please parse this Java class and return its business logic in JSON:\n\n{primary_code}"

    messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]

    args = argparse.ArgumentParser(description="Analyze Java business logic from a JSON file.")

    global CLASS_TOOL
    CLASS_TOOL = ClassCodeRetriever(code_dir)

    try_flag = True
    while try_flag:
        try_flag, messages = analyze_business_logic_json(messages)

    business_logic = messages[-1]["content"]
    try:
        print(json.dumps(business_logic, indent=2))
    except TypeError:
        print("Business logic is not a valid JSON object, attempting to clean it up...")

    # cleaned = re.sub(r"^```(?:json)?\n?|```$", "", business_logic.strip(), flags=re.MULTILINE)
    # cleaned = parse_json_from_llm_response(business_logic)
    cleaned = extract_json_from_response(business_logic)

    # write res to a output file
    output_file = "output_business_logic.json"
    with open(output_file, 'w') as f:
        json.dump(cleaned, f, indent=2)
    print(f"Business logic extracted and saved to {output_file}")

if __name__ == "__main__":
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    main()

