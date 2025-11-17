# Add custom validation helpers if needed
def validate_role(role: str):
    if role not in ["system", "user", "assistant"]:
        raise ValueError(f"Invalid role: {role}")
