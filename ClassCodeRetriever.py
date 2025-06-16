import os

class ClassCodeRetriever:
    def __init__(self, search_dir):
        self.search_dir = search_dir

    def get_class_code(self, class_name: str) -> str:
        for root, _, files in os.walk(self.search_dir):
            for file in files:
                if file == f"{class_name}.java":
                    with open(os.path.join(root, file), 'r') as f:
                        return f.read()
        return ""  # Return empty if not found
