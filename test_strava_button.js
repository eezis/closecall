const puppeteer = require('puppeteer');

(async () => {
  console.log('Starting Puppeteer test...');
  const browser = await puppeteer.launch({
    headless: false, // Show the browser for debugging
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();

  try {
    console.log('Navigating to homepage...');
    await page.goto('http://localhost:8000', { waitUntil: 'networkidle0' });

    // Take a screenshot of the homepage
    await page.screenshot({ path: 'homepage.png', fullPage: true });
    console.log('Screenshot saved as homepage.png');

    // Look for the Strava button
    const stravaButton = await page.$('.strava-login-button');

    if (stravaButton) {
      console.log('✓ Strava button found!');

      // Check if the button text is visible
      const buttonText = await page.evaluate(el => {
        const style = window.getComputedStyle(el);
        return {
          text: el.textContent,
          color: style.color,
          backgroundColor: style.backgroundColor,
          display: style.display,
          visibility: style.visibility
        };
      }, stravaButton);

      console.log('Button properties:', buttonText);

      // Check color contrast
      if (buttonText.color && buttonText.backgroundColor) {
        console.log(`Text color: ${buttonText.color}`);
        console.log(`Background color: ${buttonText.backgroundColor}`);
      }
    } else {
      console.log('✗ Strava button not found on the page');
    }

    console.log('Test completed successfully!');
  } catch (error) {
    console.error('Error during test:', error);
  } finally {
    await browser.close();
  }
})();