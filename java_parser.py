import javalang
import json

def parse_java_file(file_path):
    with open(file_path, 'r') as f:
        code = f.read()

    tree = javalang.parse.parse(code)

    class_data = []

    for path, node in tree:
        if isinstance(node, javalang.tree.ClassDeclaration):
            class_info = {
                'class_name': node.name,
                'methods': [],
                'fields': [],
                'called_methods': set(),
                'external_classes': set()
            }

            for field in node.fields:
                for decl in field.declarators:
                    class_info['fields'].append(decl.name)

            for method in node.methods:
                method_info = {
                    'name': method.name,
                    'parameters': [param.name for param in method.parameters],
                    'body_calls': []
                }

                if method.body:
                    for b_path, b_node in method:
                        if isinstance(b_node, javalang.tree.MethodInvocation):
                            method_info['body_calls'].append(b_node.member)
                            class_info['called_methods'].add(b_node.member)

                        if isinstance(b_node, javalang.tree.ClassCreator):
                            class_info['external_classes'].add(str(b_node.type.name))

                        if isinstance(b_node, javalang.tree.MemberReference):
                            if b_node.qualifier:
                                class_info['external_classes'].add(b_node.qualifier)

                class_info['methods'].append(method_info)

            class_data.append(class_info)

    return class_data


# Example usage:
if __name__ == "__main__":
    file_path = "YourJavaFile.java"  # Replace with path to your Java class
    parsed = parse_java_file(file_path)

    with open("parsed_output.json", "w") as f:
        json.dump(parsed, f, indent=2)

    print("✅ Java class parsed. Output written to parsed_output.json")
