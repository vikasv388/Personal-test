describe('Google Search', () => {

    it('should search in Google', async () => {

        await browser.url('https://www.google.com');

        const searchBox = await $('textarea[name="q"]');

        await searchBox.setValue('WebdriverIO');

        await searchBox.keys('Enter');

        await browser.pause(2000);

        await expect(browser).toHaveTitleContaining(
            'WebdriverIO'
        );

        console.log('Search completed successfully');
    });
});
