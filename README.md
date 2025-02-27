# scholarship-data-extractor
# Scholarship Data Scraper

This project automates the extraction, processing, and organization of scholarship data from websites using Selenium for web scraping and Google's Gemini AI for data structuring.

## Features

- **Web Scraping**: Extracts scholarship data from target websites
- **AI Processing**: Uses Gemini AI to structure raw data
- **Excel Export**: Saves processed data in organized Excel format
- **Automatic Class Extraction**: Identifies relevant HTML classes dynamically
- **Error Handling**: Robust retry mechanisms for API and web operations

## Requirements

- Python 3.8+
- Chrome browser
- Google Gemini API key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/qed42/scholarship-data-extractor
   cd scholarship-scraper
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Gemini API key:
   - Create a `.env` file in the project root
   - Add your API key:
     ```env
     GEMINI_API_KEY=your_api_key_here
     ```

## Usage

Run the main script:
   ```bash
   python scholarship_scraper.py
   ```
The script will:
- Launch Chrome browser
- Extract scholarship data
- Process with Gemini AI
- Save results to `scholarship_data.xlsx`

## Configuration

Edit `scholarship_scraper.py` to customize:

- `WEBSITE_URL`: Target scholarship website
- `KEYWORDS`: Class name keywords for filtering
- `OUTPUT_EXCEL`: Output file path



## Requirements

The `requirements.txt` file includes:
```txt
selenium>=4.0
google-generativeai>=0.3.0
openpyxl>=3.0
webdriver-manager>=3.0
python-dotenv>=0.19
```

## Troubleshooting

### Common Issues

**ChromeDriver Issues:**
- Ensure Chrome is updated
- Run `python -m webdriver_manager update`

**API Rate Limits:**
- Script includes exponential backoff
- Consider upgrading API quota if needed

**Website Changes:**
- Update `KEYWORDS` if class names change
- Adjust wait times if website is slow

## Contributing

1. Fork the repository
2. Create your feature branch:
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Open a pull request
