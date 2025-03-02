from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Set up Selenium WebDriver
driver = webdriver.Chrome()  # Ensure you have ChromeDriver installed
driver.get("https://www.buddy4study.com/scholarships")

# Wait for the page to load
time.sleep(5)  # Adjust the sleep time as needed

# List of class names
class_names = [
    "Listing_rightAward__DxMQV", "FilterList_filterCont__hBJSH", "slick-prev", "sticky-top", 
    "Footer_subscribeText__u40It", "FeaturedScholarship_featuredScholarships__2rGfO", 
    "slick-track", "overflow-hidden", "Menu_tabsWrapper__hS_lq", "Menu_dropdownMegaMenu__9Um9r", 
    "ScholarshipListing_scholarMiddle__aKKxg", "Menu_menuCell__fyODf", "col-md-4", "w-75", 
    "Menu_dropdownMegaMenuExplore__t5QKN", "slick-active", "col-md-2", "slick-cloned", 
    "Footer_logoBuddy__GJN_n", "col-md-8", "Menu_box1___Zh7s", "position-sticky", 
    "Listing_scholarshipsRecent__7xcMN", "Listing_categorySearch__lcoli", 
    "FilterList_filterLeft__vrjY1", "Menu_borderRight__QrGdj", "Footer_appCard__xMGya", 
    "Footer_belowFooter__VrymE", "slick-initialized", "Menu_menutitle__BR8Te", "slick-arrow", 
    "Footer_Footer__kIb0c", "slick-next", "slick-list", "featuredScholarships", "col-md-3", 
    "Menu_categoriesGrid__e58jq", "Menu_dropDiv__r0uhL", "FilterList_filterCover__Ugqq0", 
    "Listing_categoriesCard___CHju", "ScholarshipListing_scholarCont__bQXwa", 
    "Footer_subscribeDiv__uMFBV", "row", "border", "Menu_dropdownMegaMenu2__AU4Ww", 
    "Menu_headerFullWidth__aJW74", "Menu_hambergermenu__mdFbO", 
    "ScholarshipListing_scholarshipListing__2gN9C", "Listing_categoryForm__51sDC", 
    "Listing_leftAward__XSeYw", "Listing_categoriesName__ZWDqy", "slick-slide", 
    "FilterList_categoriesHeading__ZPsdK", "Menu_logoBuddy__awBCM", "Listing_calendarDate__WCgKV", 
    "ScholarshipListing_scholarLeft__84dzJ", "ScholarshipListing_scholarsRows__zLBOc", 
    "FeaturedScholarship_featuredWrapper__O8ZR1", "slick-current", "Footer_socialText__l0nW1", 
    "Menu_dropdownMegaMenu3__c375k", "jsx-baed4316bac7203", "Menu_dropdownMegaMenuAr__DrBgn", 
    "Footer_belowScholarships__GZJn_", "mt-3", "Menu_explore__nzOGi", "Footer_socialMedia__Fa4bu", 
    "slick-slider", "Footer_footerwhatappsicon__UO7wW", "col-md-5", 
    "FilterList_optionsWrapper__x_dPF", "Menu_scholarshipCategories__Y7zY4", 
    "Menu_categoriesMenu__1GJwM", "Listing_ScholarTabs__h_Y64", "Footer_footerLinks__P9Jba", 
    "Footer_secondcol__y9s_j", "borderBottom", "border-light", "Listing_categoriesPart__kpHTV", 
    "FeaturedScholarship_buddy4StudyServices__aU6lL", "Footer_footerwhatappsleft__InpoB", 
    "h-100", "Footer_textright__zTOyb", "Menu_categoriesCol___q0e9", "Menu_alignCenter__DGa5p", 
    "featuredScholarshipsAlternatetwo", "Menu_studentServicesDiv__oUMX4", "Footer_top__zw0uT", 
    "mx-auto", "Footer_scholarshipsCol__rc5Eu", "col-md-7", "col-md-12", 
    "FilterList_categoriesClass__u7Ohn", "full-width-container", "Listing_daystoGo__mTJ17", 
    "Menu_displayNone__vzHr3", "w-100", "header-fixed", "Listing_categoriesRight__7Zjyu", 
    "Footer_firstcol__sTX8i", "container-true", "Menu_box2__FJpLE", "Menu_flexDir__KSiG3", 
    "posrelative", "ScholarshipListing_scholarRight__XHL0_", "goolgediv", "Listing_awardCont__qnjQK"
]

# Dictionary to store data
data = {}

# Extract data for each class
for class_name in class_names:
    try:
        elements = driver.find_elements(By.CLASS_NAME, class_name)
        if elements:
            data[class_name] = [element.text for element in elements]
    except Exception as e:
        print(f"Error extracting data for class {class_name}: {e}")

# Save data to a text file
with open("extracted_data.txt", "w", encoding="utf-8") as f:
    for class_name, content in data.items():
        f.write(f"Class: {class_name}\n")
        for text in content:
            f.write(f"{text}\n")
        f.write("\n" + "="*50 + "\n")

print("Data extraction complete. Saved to extracted_data.txt")

# Close the browser
driver.quit()