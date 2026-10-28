import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public class FirstSeleniumTest {

    public static void main(String[] args) {

        // Open Chrome
        WebDriver driver = new ChromeDriver();

        // Open Google
        driver.get("https://www.google.com");

        // Find search box and type
        driver.findElement(By.name("q")).sendKeys("Selenium Java");

        // Press Enter
        driver.findElement(By.name("q")).submit();

        // Print page title
        System.out.println("Page Title: " + driver.getTitle());

        // Close browser
        driver.quit();
    }
}
