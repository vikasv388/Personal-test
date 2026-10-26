import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;

public class SeleniumDemo {

    public static void main(String[] args) {

        // Launch Chrome browser
        WebDriver driver = new ChromeDriver();

        // Open a website
        driver.get("https://www.google.com");

        // Maximize the browser window
        driver.manage().window().maximize();

        // Find the search box
        WebElement searchBox = driver.findElement(
            By.name("q")
        );

        // Enter text
        searchBox.sendKeys("Java Selenium");

        // Submit the search
        searchBox.submit();

        // Print the page title
        System.out.println("Page title: " + driver.getTitle());

        // Close the browser
        driver.quit();
    }
}
