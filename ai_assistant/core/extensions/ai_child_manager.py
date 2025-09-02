# AI child management module

def create_ai_child(config):
    import json, os
    ai_name = config.get("name", "default_child")
    info = {
        "modules": config.get("modules", []),
        "inherited": config.get("inherited", []),
        "new": config.get("new", [])
    }
    os.makedirs(f"ai_children/{ai_name}", exist_ok=True)
    with open(f"ai_children/{ai_name}/ai_info.json", "w") as f:
        json.dump(info, f)
    return f"AI child '{ai_name}' created."