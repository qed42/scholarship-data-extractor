import google.generativeai as genai
import openpyxl
import time
import random
from google.api_core.exceptions import ResourceExhausted
import re

# Set up Gemini API
API_KEY = ""  # Replace with your Gemini API key
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")

def retry_with_backoff(func, max_retries=5):
    """Retry a function with exponential backoff when rate limited."""
    for attempt in range(max_retries):
        try:
            return func()
        except ResourceExhausted as e:
            if attempt == max_retries - 1:
                raise e
            
            wait_time = (2 ** attempt) + random.random()
            print(f"Rate limit exceeded. Waiting {wait_time:.2f} seconds (attempt {attempt+1}/{max_retries})...")
            time.sleep(wait_time)
    
    # This should never be reached due to the exception handling above
    return func()

def chunk_text(text, max_length=4000):
    """Split text into chunks of maximum length."""
    words = text.split()
    chunks = []
    current_chunk = []
    
    current_length = 0
    for word in words:
        if current_length + len(word) + 1 > max_length:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_length = len(word)
        else:
            current_chunk.append(word)
            current_length += len(word) + 1  # +1 for space
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def process_scholarship_data():
    # Read the extracted data from the text file
    try:
        with open("extracted_data_with_links.txt", "r", encoding="utf-8") as f:
            extracted_data = f.read()
    except FileNotFoundError:
        print("Error: File 'extracted_data_with_links.txt' not found.")
        return
    
    # Check if data needs to be chunked
    if len(extracted_data) > 4000:
        print("Data is large, processing in chunks...")
        data_chunks = chunk_text(extracted_data)
        all_structured_data = []
        
        for i, chunk in enumerate(data_chunks):
            print(f"Processing chunk {i+1}/{len(data_chunks)}...")
            
            prompt = f"""The following data is part {i+1} of {len(data_chunks)} extracted from a webpage and contains scholarship-related information. 
            Please organize it into a structured format with each scholarship on a single line using pipe delimiters (|).
            Format each line as: Scholarship Name|Eligibility|Deadline|Amount|Application Link
            
            Here is the data:
            {chunk}
            """
            
            def get_response():
                response = model.generate_content(prompt)
                return response.text
            
            try:
                structured_chunk = retry_with_backoff(get_response)
                all_structured_data.append(structured_chunk)
                # Add a delay between chunks to avoid rate limits
                if i < len(data_chunks) - 1:
                    time.sleep(2)
            except Exception as e:
                print(f"Error processing chunk {i+1}: {str(e)}")
        
        structured_data = "\n".join(all_structured_data)
    else:
        prompt = f"""The following data is extracted from a webpage and contains scholarship-related information. 
        Please organize it into a structured format with each scholarship on a single line using pipe delimiters (|).
        Format each line as: Scholarship Name|Eligibility|Deadline|Amount|Application Link
        
        Here is the data:
        {extracted_data}
        """
        
        def get_response():
            response = model.generate_content(prompt)
            return response.text
        
        try:
            structured_data = retry_with_backoff(get_response)
        except Exception as e:
            print(f"Error: {str(e)}")
            return
    
    # Save the structured data to an Excel file
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Scholarship Data"
    
    # Add headers
    sheet.append(["Scholarship Name", "Eligibility", "Deadline", "Amount", "Application Link"])
    
    # Parse the structured data and write to Excel
    line_count = 0
    for line in structured_data.split("\n"):
        line = line.strip()
        # Skip empty lines and header rows
        if not line or line.startswith("Scholarship Name") or line.startswith("-") or "|" not in line:
            continue
        
        # Try to split by pipe delimiter
        parts = line.split("|")
        if len(parts) == 5:
            sheet.append([part.strip() for part in parts])
            line_count += 1
        else:
            print(f"Warning: Skipping improperly formatted line: {line}")
    
    # Save the Excel file
    try:
        workbook.save("scholarship_data.xlsx")
        print(f"Success! {line_count} scholarships have been saved to scholarship_data.xlsx")
    except Exception as e:
        print(f"Error saving Excel file: {str(e)}")

if __name__ == "__main__":
    process_scholarship_data()