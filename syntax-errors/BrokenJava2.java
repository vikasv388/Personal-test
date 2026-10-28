public class BrokenJava2 {
    public static void main(String[] args) {
        int[] scores = {82, 91, 76};
        int total = 0;

        for (int score : scores) {
            total += score;
        }

        double average = total / scores.length
        System.out.println("Average score: " + average);
    }
}
