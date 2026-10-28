import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;

public class EasySelenium {
    public static void main(String[] args) {

        // Open Chrome browser
        WebDriver driver = new ChromeDriver();

        // Open a website
        driver.get("https://www.google.com");

        // Print page title
        System.out.println(driver.getTitle());

        // Find search box and enter text
        WebElement searchBox = driver.findElement(By.name("q"));
        searchBox.sendKeys("Java Selenium");

        // Press Enter
        searchBox.submit();

        // Close browser
        driver.quit();
    }
}
