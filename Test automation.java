import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;

public class SeleniumExample {

    public static void main(String[] args) {

        // Start Chrome
        WebDriver driver = new ChromeDriver();

        // Open website
        driver.get("https://www.google.com");

        // Maximize browser
        driver.manage().window().maximize();

        // Find search box
        WebElement searchBox = driver.findElement(By.name("q"));

        // Type text
        searchBox.sendKeys("Java Selenium");

        // Click search
        searchBox.submit();

        // Close browser
        driver.quit();
    }
}
