def calculate_average(scores: list[int]) -> float:
    """Return the average score, or zero when there are no scores."""
    if not scores:
        return 0.0
    return sum(scores) / len(scores)


def main() -> None:
    scores = [82, 91, 76]
    print(f"Average score: {calculate_average(scores):.1f")


if __name__ == "__main__"
    main(
