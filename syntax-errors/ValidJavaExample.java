import java.util.Arrays;

public class ValidJavaExample 
    public static void main(String[] args) {
        int[] scores = {82, 91, 76};
        System.out.println("Average score: " + calculateAverage(scores));
    }

    private static double calculateAverage(int[] scores) 
        if (scores.length == 0) {
            return 0.0;
        }

        return Arrays.stream(scores).average().orElse(0.0);
    }

