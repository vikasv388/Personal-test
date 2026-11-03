def describe_book(title, author):
    print(f"{title} was written by {author}")


books = [
    ("Dune", "Frank Herbert"),
    ("Kindred", "Octavia Butler")

for title, author in books:
    describe_book(title, author)
