from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import requests
import base64

def open_whatsapp(driver):
    driver.get("https://web.whatsapp.com")
    # print("Scan the QR code if required...")
    time.sleep(5)


def _get_driver():
    # Set up WebDriver
    options = webdriver.ChromeOptions()
    # options.add_argument(f"--user-data-dir=./whatsapp_profile_{int(time.time())}")  # Unique profile directory
    options.add_argument("--user-data-dir=./whatsapp_profile")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver



def main():
    driver = _get_driver()
    open_whatsapp(driver)
    search_elem_div = driver.find_element(By.CSS_SELECTOR, '[aria-label="Cuadro de texto para ingresar la búsqueda"]')
    search_elem = search_elem_div.find_element(By.TAG_NAME, 'p')
    search_elem.send_keys("LCB 24/25 - General")
    time.sleep(5)
    div_with_results = driver.find_element(By.CSS_SELECTOR, '[aria-label="Resultados de la búsqueda."]')
    results = div_with_results.find_elements(By.CSS_SELECTOR, '[role="listitem"]')
    results[1].click()
    time.sleep(2)
    for _ in range(3):
        driver.execute_script("""
            const div = document.querySelector('[role="application"]');
            div.parentElement.scrollTop = 0;
        """)
        time.sleep(1)
    index = 0
    pictures_paths_and_texts = []
    for msg_with_image in driver.find_elements(By.CSS_SELECTOR, '[aria-label="Abrir foto"]'):
        for img in msg_with_image.find_elements(By.TAG_NAME, 'img'):
            index += 1
            img_alt = img.get_attribute("alt")
            src = img.get_attribute("src")
            if src and src.startswith("blob:"):
                javascript_code = f"""
                    var imgUrl = "{src}";

                    var newImage = new Image();
newImage.crossOrigin = "Anonymous"; // For CORS
newImage.src = imgUrl;

// Return a Promise to handle the async nature of image loading
return new Promise(function(resolve, reject) {{
    newImage.onload = function() {{
        var canvas = document.createElement('canvas');
        var ctx = canvas.getContext('2d');
        canvas.width = newImage.width;
        canvas.height = newImage.height;
        ctx.drawImage(newImage, 0, 0);
        var base64String = canvas.toDataURL('image/png');
        resolve(base64String);  // This will return the base64 string to Python
    }};
    newImage.onerror = reject;  // Handle error case
}});

                """
                base64_string = driver.execute_script(javascript_code)
                if base64_string.startswith("data:image/png;base64,"):
                    base64_string = base64_string.replace("data:image/png;base64,", "")
                image_data = base64.b64decode(base64_string)
                output_file_path = f"whatsapp_image_{index}.png"
                with open(output_file_path, "wb") as image_file:
                    image_file.write(image_data)
                pictures_paths_and_texts.append((output_file_path, img_alt))
    return pictures_paths_and_texts


if __name__ == "__main__":
    main()