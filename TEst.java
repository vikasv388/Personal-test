
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.support.ui.ExpectedConditions;
import java.time.Duration;

public class SeleniumDemo {

    public static void main(String[] args) {

        WebDriver driver = new ChromeDriver();

        try {
            driver.manage().window().maximize();
            driver.get("https://www.google.com");

            WebDriverWait wait = new WebDriverWait(
                driver, Duration.ofSeconds(10)
            );

            WebElement searchBox = wait.until(
                ExpectedConditions.visibilityOfElementLocated(
                    By.name("q")
                )
            );

            searchBox.sendKeys("Java Selenium Tutorial");
            searchBox.submit();

            wait.until(
                ExpectedConditions.titleContains("Java Selenium")
            );

            System.out.println("Page Title: " + driver.getTitle());

        } finally {
            driver.quit();
        }
    }
}
