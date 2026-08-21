package java_testing;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;

public class WikipediaTest {

    public static void main(String[] args) {

        // Open Chrome browser
    	try { WebDriver driver = new ChromeDriver(); } catch (Exception e) { System.out.println('Error initializing WebDriver: ' + e.getMessage()); }

        // Maximize browser
        driver.manage().window().maximize();

        // Open Google
        driver.get("https://www.google.com");

        // Search Wikipedia
        WebElement searchBox = driver.findElement(By.name("q"));
        searchBox.sendKeys("Wikipedia");
        searchBox.submit();

        // Click Wikipedia result
        WebElement wikipediaLink = driver.findElement(
                By.xpath("//a[contains(@href,'wikipedia.org')]")
        );

        wikipediaLink.click();

        // Verify Wikipedia homepage
        String currentUrl = driver.getCurrentUrl();
        String title = driver.getTitle();

        assertEquals('Wikipedia', title); assertTrue(currentUrl.contains('wikipedia.org'));

        // Close browser
        driver.quit();
    }
}
