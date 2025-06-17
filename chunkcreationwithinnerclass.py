import os
import re

def is_method_signature(line):
    return re.match(r'\s*(public|private|protected)?\s+(static\s+)?[\w<>\[\]]+\s+\w+\s*\([^)]*\)\s*[{]?', line) \
        or re.match(r'\s*(public|private|protected)?\s*\w+\s*\([^)]*\)\s*[{]?', line)

def extract_package_imports(lines):
    package_imports = []
    other_lines = []
    for line in lines:
        if line.strip().startswith("package ") or line.strip().startswith("import "):
            package_imports.append(line)
        else:
            other_lines.append(line)
    return package_imports, other_lines

def extract_classes(lines):
    """
    Finds all class/inner class blocks using brace matching
    """
    class_blocks = []
    current_block = []
    inside_class = False
    brace_depth = 0

    for line in lines:
        if not inside_class and re.search(r'\b(class|interface|enum)\b', line):
            inside_class = True
            current_block = [line]
            brace_depth = line.count("{") - line.count("}")
            continue

        if inside_class:
            current_block.append(line)
            brace_depth += line.count("{") - line.count("}")
            if brace_depth <= 0:
                inside_class = False
                class_blocks.append(current_block)
                current_block = []

    return class_blocks

def chunk_class_block(class_lines, max_chunk_lines):
    chunks = []
    header = []
    fields = []
    methods = []
    inner_classes = []
    inside_method = False
    brace_depth = 0
    current_method = []
    inside_inner_class = False
    current_inner_class = []

    for i, line in enumerate(class_lines):
        stripped = line.strip()
        if re.search(r'\b(class|interface|enum)\b', stripped) and '{' in stripped and not inside_method:
            inside_inner_class = True
            current_inner_class = [line]
            brace_depth = line.count('{') - line.count('}')
            continue

        if inside_inner_class:
            current_inner_class.append(line)
            brace_depth += line.count('{') - line.count('}')
            if brace_depth <= 0:
                inside_inner_class = False
                inner_classes.append(current_inner_class)
                current_inner_class = []
            continue

        if is_method_signature(line) and not inside_method:
            inside_method = True
            current_method = [line]
            brace_depth = line.count('{') - line.count('}')
            continue

        if inside_method:
            current_method.append(line)
            brace_depth += line.count('{') - line.count('}')
            if brace_depth <= 0:
                inside_method = False
                methods.append(current_method)
                current_method = []
        else:
            if not line.strip().startswith('@') and ';' in line:
                fields.append(line)
            else:
                header.append(line)

    # Chunking
    current_chunk = []
    current_len = len(header) + len(fields) + 2  # class { }
    for method in methods:
        if current_len + len(method) > max_chunk_lines and current_chunk:
            chunks.append(current_chunk)
            current_chunk = []
            current_len = len(header) + 2
        current_chunk.extend(method)
        current_len += len(method)

    if current_chunk:
        chunks.append(current_chunk)

    # Build final chunk strings
    final_chunks = []
    for i, chunk_body in enumerate(chunks):
        chunk = []
        chunk.extend(header)
        chunk.append("{")
        if i == 0:
            chunk.extend(fields)
        chunk.extend(chunk_body)
        for inner_class in inner_classes:
            chunk.extend(inner_class)
        chunk.append("}")
        final_chunks.append('\n'.join(chunk))

    return final_chunks

def chunk_java_with_inner_classes(code: str, max_chunk_lines: int):
    lines = code.split('\n')
    package_imports, code_lines = extract_package_imports(lines)
    class_blocks = extract_classes(code_lines)

    all_chunks = []
    for class_block in class_blocks:
        chunks = chunk_class_block(class_block, max_chunk_lines)
        for chunk in chunks:
            full_chunk = '\n'.join(package_imports) + '\n\n' + chunk
            all_chunks.append(full_chunk)

    return all_chunks


# with open("MyComplexClass.java") as f:
   #  java_code = f.read()

# chunks = chunk_java_with_inner_classes(java_code, max_chunk_lines=120)

# for i, chunk in enumerate(chunks):
   #  with open(f"MyComplexClass_Chunk{i+1}.java", "w") as f:
       #  f.write(chunk)

