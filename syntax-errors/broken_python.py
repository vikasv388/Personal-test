def greet(name)
    print(f"Hello, {name}!")


def add_numbers(first, second):
    return first + second


def main():
    names = ["Ava", "Noah", "Mia"]
    for name in names:
        greet(name)

    total = add_numbers(4, 7)
    print(f"Total: {total}")


main()
