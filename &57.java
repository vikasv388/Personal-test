import java.util.Scanner;

class Student 
    public static void main(String[] args) 

        Scanner sc = new Scanner(System.in);

        String name;
        int roll, age;
        double marks;

        System.out.print("Enter student name: ");
        name = sc.nextLine();

        System.out.print("Enter roll number: ");
        roll = sc.nextInt();

        System.out.print("Enter age: ");
        age = sc.nextInt();

        System.out.print("Enter marks: ");
        marks = sc.nextDouble();

        System.out.println("\n--- Student Details ---");

        System.out.println("Name: " + name);
        System.out.println("Roll Number: " + roll);
        System.out.println("Age: " + age);
        System.out.println("Marks: " + marks);

        if (marks >= 90) {
            System.out.println("Grade: A");
        }
        else if (marks >= 75) {
            System.out.println("Grade: B");
        }
        else if (marks >= 60) {
            System.out.println("Grade: C");
        }
        else {
            System.out.println("Grade: D");
        }

        if (marks  40) 
            System.out.println("Result: Pass");
        
        else {
            System.out.println("Result: Fail");
        }

        sc.close();
    }
}
