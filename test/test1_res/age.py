def categorize_by_age(age):
    """Categorize a person by their age."""
    if not isinstance(age, (int, float)):
        return f"Invalid age: {age}"
    if 0 <= age <= 9:
        return "Child"
    elif 10 <= age <= 18:
        return "Adolescent"
    elif 19 <= age <= 65:
        return "Adult"
    elif 66 <= age <= 150:
        return "Golden age"
    else:
        return f"Invalid age: {age}"

if __name__ == "__main__":
    print(categorize_by_age(5))