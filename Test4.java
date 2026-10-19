import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

public class HandleWebPage {

    public static void main(String[] args) {

        // Launch Chrome browser
        WebDriver driver = new ChromeDriver();

        try {
            // Maximize the browser window
            driver.manage().window().maximize();

            // Open website
            driver.get("https://www.google.com");

            // Explicit wait
            WebDriverWait wait = new WebDriverWait(
                driver, Duration.ofSeconds(10)
            );

            // Locate search box
            WebElement searchBox = wait.until(
                ExpectedConditions.visibilityOfElementLocated(
                    By.name("q")
                )
            );

            // Enter text
            searchBox.sendKeys("Java Selenium tutorial");

            // Submit search
            searchBox.submit();

            // Wait for page title
            wait.until(
                ExpectedConditions.titleContains("Java Selenium")
            );

            // Print page details
            System.out.println("Page title: " + driver.getTitle());
            System.out.println("Current URL: " + driver.getCurrentUrl());

        } finally {
            // Close browser and end session
            driver.quit();
        }
    }
}
