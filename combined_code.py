# scholarship_scraper.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import google.generativeai as genai
import openpyxl
import time
import random
from webdriver_manager.chrome import ChromeDriverManager
from google.api_core.exceptions import ResourceExhausted

# Configuration
WEBSITE_URL = "https://www.buddy4study.com/scholarships"
GEMINI_API_KEY = "YOUR_API_KEY"  # Replace with your API key
OUTPUT_EXCEL = "scholarship_data.xlsx"
KEYWORDS = {'scholar', 'listing', 'deadline', 'award', 'amount', 'apply', 'grant'}

# Initialize Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")

def initialize_driver():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()
    return driver

def extract_classes(driver):
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'Scholarship')]"))
    )
    elements = driver.find_elements(By.XPATH, "//*[@class]")
    return {cls for element in elements for cls in element.get_attribute("class").split()}

def filter_classes(class_set):
    return [cls for cls in class_set if any(kw in cls.lower() for kw in KEYWORDS)]

def scrape_data(driver, class_list):
    data = {}
    for class_name in class_list:
        try:
            elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, class_name))
            )
            data[class_name] = []
            for element in elements:
                text = element.text.strip()
                links = [
                    f"{link.text.strip()}: {link.get_attribute('href')}"
                    for link in element.find_elements(By.TAG_NAME, "a")
                    if link.get_attribute('href')
                ]
                data[class_name].append({"text": text, "links": links})
        except Exception as e:
            print(f"Skipping {class_name}: {str(e)}")
    return data

def retry_with_backoff(func, max_retries=5):
    for attempt in range(max_retries):
        try:
            return func()
        except ResourceExhausted:
            if attempt == max_retries - 1:
                raise
            wait = (2 ** attempt) + random.random()
            print(f"Retrying in {wait:.1f}s...")
            time.sleep(wait)
    return func()

def process_with_gemini(data):
    prompt = """Organize this scholarship data into pipe-delimited format:
    Scholarship Name|Eligibility|Deadline|Amount|Application Link
    
    Raw Data:
    {data}
    
    Return only properly formatted lines. Skip incomplete entries."""
    
    try:
        response = retry_with_backoff(lambda: model.generate_content(prompt.format(data=str(data))))
        return response.text
    except Exception as e:
        print(f"AI Processing failed: {str(e)}")
        return ""

def save_to_excel(structured_data):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Scholarships"
    ws.append(["Scholarship Name", "Eligibility", "Deadline", "Amount", "Application Link"])
    
    count = 0
    for line in structured_data.split('\n'):
        if not line or '|' not in line or line.startswith(('Scholarship', '-')):
            continue
        parts = [p.strip() for p in line.split('|', 4)][:5]
        if len(parts) == 5:
            ws.append(parts)
            count += 1
    
    wb.save(OUTPUT_EXCEL)
    print(f"Saved {count} scholarships to {OUTPUT_EXCEL}")

def main():
    driver = initialize_driver()
    try:
        driver.get(WEBSITE_URL)
        
        # Phase 1: Extract and filter classes
        all_classes = extract_classes(driver)
        relevant_classes = filter_classes(all_classes)
        print(f"Identified {len(relevant_classes)} relevant classes")
        
        # Phase 2: Data scraping
        scraped_data = scrape_data(driver, relevant_classes)
        
        # Phase 3: AI Processing
        structured_data = process_with_gemini(scraped_data)
        
        # Phase 4: Save results
        if structured_data:
            save_to_excel(structured_data)
            
    finally:
        driver.quit()
        print("Process completed")

if __name__ == "__main__":
    main()