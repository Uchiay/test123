import os
import re
import openai
from typing import List, Dict

# 1. CONFIGURATION
openai.api_key = "your-openai-key"
CODE_DIR = "./java_sources"
CHUNK_SIZE = 200  # Number of lines per chunk

# 2. TOOL: Fetch class code by name
def get_class_code(class_name: str) -> str:
    for root, _, files in os.walk(CODE_DIR):
        for file in files:
            if file == f"{class_name}.java":
                with open(os.path.join(root, file), "r") as f:
                    return f.read()
    return f"// Class {class_name} not found"

# 3. CHUNKING FUNCTION
def chunk_code(code: str, chunk_size: int = CHUNK_SIZE) -> List[str]:
    lines = code.splitlines()
    chunks = ["\n".join(lines[i:i + chunk_size]) for i in range(0, len(lines), chunk_size)]
    return chunks

# 4. PARSE JAVA FILE
def preprocess_java_code(code: str) -> Dict:
    class_name = re.search(r"class\s+(\w+)", code)
    methods = re.findall(r"(?s)(/\*\*.*?\*/)?\s*(public|protected|private|static|\s)+[\w<>,\[\]]+\s+(\w+)\s*\((.*?)\)\s*\{", code)
    annotations = re.findall(r"@\w+", code)

    parsed_methods = []
    for comment, modifier, name, params in methods:
        parsed_methods.append({
            "name": name,
            "signature": f"{modifier.strip()} {name}({params.strip()})",
            "comment": comment.strip() if comment else None
        })

    return {
        "class_name": class_name.group(1) if class_name else None,
        "methods": parsed_methods,
        "annotations": annotations
    }

# 5. TOOL WRAPPER FOR TOOL CALLING (Simulating tool usage for now)
def handle_tool_call(class_name: str) -> List[dict]:
    class_code = get_class_code(class_name)
    class_chunks = chunk_code(class_code)
    return [
        {
            "role": "tool",
            "name": "get_class_code",
            "content": chunk
        }
        for chunk in class_chunks
    ]

# 6. PROMPT CONSTRUCTION (Messages)
def construct_messages(main_class_code: str, dependent_classes: List[str]) -> List[dict]:
    messages = [
        {
            "role": "system",
            "content": (
                "You are a software analyst. Your task is to extract business logic from Java classes.\n"
                "Given Java class code, identify and summarize business rules, including conditions, actions,\n"
                "and involved entities. Return structured JSON like:\n"
                "{ \"className\": ..., \"businessRules\": [ {description, condition, action, relatedEntities} ] }"
            )
        }
    ]

    # Chunk main class code
    main_chunks = chunk_code(main_class_code)
    for i, chunk in enumerate(main_chunks):
        messages.append({
            "role": "user",
            "content": f"Part {i+1} of main class code:\n\n{chunk}"
        })

    # Add dependent classes
    for dep_class in dependent_classes:
        tool_msgs = handle_tool_call(dep_class)
        messages.extend(tool_msgs)

    return messages

# 7. INVOKE LLM

def analyze_business_logic(main_class: str, dependencies: List[str]):
    main_class_code = get_class_code(main_class)
    messages = construct_messages(main_class_code, dependencies)

    response = openai.ChatCompletion.create(
        model="gpt-4o",  # or use gpt-4-1106-preview
        messages=messages,
        temperature=0.2
    )

    return response.choices[0].message.content

# 8. USAGE EXAMPLE
if __name__ == "__main__":
    main_class_code = get_class_code("InvoiceProcessor")
    parsed = preprocess_java_code(main_class_code)
    print("\n=== Parsed Java Code Metadata ===\n")
    print(parsed)

    result = analyze_business_logic("InvoiceProcessor", ["Customer", "Order"])
    print("\n=== Extracted Business Logic JSON ===\n")
    print(result)
