from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Set up Selenium WebDriver
driver = webdriver.Chrome()  # Ensure you have ChromeDriver installed
driver.get("https://www.buddy4study.com/scholarships")   #chane your name of the website here

# Wait for the page to load
time.sleep(5)  # Adjust the sleep time as needed

# Extract all div elements and their classes
div_elements = driver.find_elements(By.TAG_NAME, "div")

# Use a set to store unique classes
unique_classes = set()

# Collect all unique classes
for div in div_elements:
    classes = div.get_attribute("class")
    if classes:
        # Split multiple classes (if any) and add them to the set
        for cls in classes.split():
            unique_classes.add(cls)

# Write unique classes to a text file
with open("div_classes.txt", "w", encoding="utf-8") as f:
    for cls in unique_classes:
        f.write(f"{cls}\n")

print(f"Found {len(unique_classes)} unique classes. Saved to div_classes.txt")

# Close the browser
driver.quit()