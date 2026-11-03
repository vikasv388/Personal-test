void main() {
  final names = ['Ava', 'Noah', 'Mia'];

  for (final name in names) {
    greet(name);
  }

  final total = addNumbers(4, 7);
  print('Total: $total');
  print('This line is missing a semicolon')
}

void greet(String name) {
  print('Hello, $name!');
}

int addNumbers(int first, int second) {
  return first + second;
}
