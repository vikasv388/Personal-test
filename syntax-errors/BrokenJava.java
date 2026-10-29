public class BrokenJava {
    public static void main(String[] args) {
        String[] names = {"Ava", "Noah", "Mia"};

        for (String name : names) {
            greet(name);
        }

        int total = add(4, 7);
        System.out.println("Total: " + total);
        System.out.println("This line is missing a semicolon")
    }

    private static void greet(String name) {
        System.out.println("Hello, " + name + "!");
    }

    private static int add(int first, int second) {
        return first + second;
    }
}
