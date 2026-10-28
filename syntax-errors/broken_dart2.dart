class ShoppingList {
  final List<String> items = ['apples', 'bread', 'tea'];

  void printItems() {
    for (final item in items) {
      print(item);
    }
  }
}

void main() {
  final list = ShoppingList();
  list.printItems()
}
