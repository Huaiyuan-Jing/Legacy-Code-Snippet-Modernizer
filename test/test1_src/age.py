# 文件：age.py (源于 Python 2)
def categorize_by_age(age):
    # Python 2 中的逻辑实现
    if age >= 0 and age <= 9:
        return "Child"
    elif age > 9 and age <= 18:
        return "Adolescent"
    elif age > 18 and age <= 65:
        return "Adult"
    elif age > 65 and age <= 150:
        return "Golden age"
    else:
        return "Invalid age: %s" % age

if __name__ == "__main__":
    # Python 2 中打印
    print categorize_by_age(5)
