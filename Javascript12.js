
const { chromium } = require('playwright');

(async () => 
    // Launch browser
    const browser = await chromium.launch({
        headless: false


    // Create page
    const page = await browser.newPage();

    // Open website
    await page.goto('https://www.google.com');

    // Enter text into search box
    await page.locator('textarea[name="q"]').fill('JavaScript Playwright');

    // Press Enter
    await page.locator('textarea[name="q"]').press('Enter');

    // Wait for page to load
    await page.waitForLoadState('domcontentloaded');

    // Print page title
    console.log('Page title:', await page.title());

    // Print current URL
    console.log('Current URL:', page.url(

    // Close browser
    await browser.close();
