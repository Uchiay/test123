import os
import re

def is_method_signature(line):
    return re.match(r'\s*(public|private|protected)?\s+(static\s+)?[\w<>\[\]]+\s+\w+\s*\([^)]*\)\s*[{]?', line) \
           or re.match(r'\s*(public|private|protected)?\s*\w+\s*\([^)]*\)\s*[{]?', line)  # Constructor

def chunk_java_by_method_and_size(java_code: str, max_chunk_lines: int):
    lines = java_code.split('\n')
    package_import_lines = []
    class_header_lines = []
    field_lines = []
    method_chunks = []
    current_method = []
    current_chunk = []
    brace_count = 0
    in_method = False
    found_class = False
    class_decl_started = False

    for line in lines:
        stripped = line.strip()

        # Handle package & import
        if stripped.startswith('package ') or stripped.startswith('import '):
            package_import_lines.append(line)
            continue

        # Detect class start
        if re.match(r'.*\bclass\b.*{?', stripped) and not class_decl_started:
            class_header_lines.append(line)
            class_decl_started = True
            if '{' in stripped:
                found_class = True
            continue
        elif class_decl_started and not found_class:
            class_header_lines.append(line)
            if '{' in stripped:
                found_class = True
            continue

        if not found_class:
            continue  # wait until inside class

        # Check method signature
        if is_method_signature(line) and not in_method:
            if current_method:
                method_chunks.append(current_method)
                current_method = []

            current_method = [line]
            in_method = True
            brace_count = line.count('{') - line.count('}')
            continue

        if in_method:
            current_method.append(line)
            brace_count += line.count('{') - line.count('}')
            if brace_count <= 0:
                in_method = False
                method_chunks.append(current_method)
                current_method = []
        else:
            # class-level fields, outside methods
            field_lines.append(line)

    if current_method:
        method_chunks.append(current_method)

    # Now group method_chunks into chunks based on size
    final_chunks = []
    current_chunk = []
    current_length = len(package_import_lines) + len(class_header_lines) + len(field_lines) + 2  # class + opening brace

    for method in method_chunks:
        if current_length + len(method) > max_chunk_lines and current_chunk:
            final_chunks.append(current_chunk)
            current_chunk = []
            current_length = len(package_import_lines) + len(class_header_lines) + 2  # For next chunk (no field lines)
        current_chunk.extend(method)
        current_length += len(method)

    if current_chunk:
        final_chunks.append(current_chunk)

    # Reassemble each chunk
    chunks = []
    for idx, body in enumerate(final_chunks):
        chunk = []
        chunk.extend(package_import_lines)
        chunk.append("")  # spacer
        chunk.extend(class_header_lines)
        chunk.append("{")
        if idx == 0:
            chunk.extend(field_lines)
        chunk.extend(body)
        chunk.append("}")
        chunks.append('\n'.join(chunk))

    return chunks
