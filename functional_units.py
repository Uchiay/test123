import networkx as nx

def build_functional_units(parsed_class_data):
    G = nx.DiGraph()

    for clazz in parsed_class_data:
        for method in clazz["methods"]:
            method_name = method["name"]
            G.add_node(method_name)
            for called in method["body_calls"]:
                G.add_edge(method_name, called)

    # Use weakly connected components to group functions
    components = list(nx.weakly_connected_components(G))
    functional_units = []

    for i, comp in enumerate(components):
        functional_units.append({
            "functional_unit": f"Unit {i+1}",
            "methods": list(comp)
        })

    return functional_units


# Example usage
if __name__ == "__main__":
    import json

    with open("parsed_output.json", "r") as f:
        parsed_data = json.load(f)

    functional_units = build_functional_units(parsed_data)

    with open("functional_units.json", "w") as f:
        json.dump(functional_units, f, indent=2)

    print("✅ Functional units written to functional_units.json")
