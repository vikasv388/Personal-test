double calculateAverage(List<int> scores) {
  if (scores.isEmpty) {
    return 0;
  }

  final total = scores.reduce((first, second) => first + second);
  return total / scores.length;


void main(
  final scores = [82, 91, 76];
  final average = calculateAverage(scores);
  print('Average score: ${average.toStringAsFixed(1)');
}
