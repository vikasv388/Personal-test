import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public class SeleniumTest {
    public static void main(String[] args) {

        WebDriver driver = new ChromeDriver();

        // Open website
        driver.get("https://www.google.com")

        // Print page title
        System.out.println("Page Title: " + driver.getTitle())

        // Print current URL
        System.out.println("Page URL: " + driver.getCurrentUrl());

        // Close browser
        driver.quit();
    }
}
