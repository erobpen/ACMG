#!/usr/bin/env python3
"""
Savile Row Automation Script with Selenium, OCR, and File Processing
"""

import os
import time
import subprocess
import logging
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image, ImageGrab
import pyautogui
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SavilleRowAutomation:
    def __init__(self, savillerow_path="./savillerow"):
        self.savillerow_path = Path(savillerow_path)
        self.driver = None
        self.trocr_processor = None
        self.trocr_model = None
        self.setup_trocr()
    
    def setup_trocr(self):
        """Initialize TrOCR model for text extraction"""
        try:
            logger.info("Loading TrOCR model...")
            self.trocr_processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-printed")
            self.trocr_model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-printed")
            logger.info("TrOCR model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load TrOCR model: {e}")
            raise
    
    def setup_selenium(self, headless=False):
        """Setup Selenium WebDriver"""
        try:
            chrome_options = Options()
            if headless:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            self.driver = webdriver.Chrome(options=chrome_options)
            logger.info("Selenium WebDriver initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Selenium: {e}")
            raise
    
    def click_screen(self, x, y, double_click=False):
        """Click on screen at specified coordinates"""
        try:
            if double_click:
                pyautogui.doubleClick(x, y)
                logger.info(f"Double-clicked at ({x}, {y})")
            else:
                pyautogui.click(x, y)
                logger.info(f"Clicked at ({x}, {y})")
            time.sleep(0.5)
        except Exception as e:
            logger.error(f"Failed to click at ({x}, {y}): {e}")
    
    def read_file_contents(self, filepath):
        """Read contents of a file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                logger.info(f"Read {len(content)} characters from {filepath}")
                return content
        except Exception as e:
            logger.error(f"Failed to read file {filepath}: {e}")
            return None
    
    def run_savillerow(self, essence_file, param_file, output_dir="output"):
        """Run Savile Row with essence and parameter files"""
        try:
            # Ensure we're in the correct directory
            os.chdir(self.savillerow_path)
            
            # Construct the command
            cmd = [
                "java", "-jar", "savilerow.jar",
                essence_file,
                param_file,
                "-out-dir", output_dir,
                "-run-solver"
            ]
            
            logger.info(f"Running Savile Row command: {' '.join(cmd)}")
            
            # Run the command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            logger.info(f"Savile Row exit code: {result.returncode}")
            logger.info(f"Stdout: {result.stdout}")
            if result.stderr:
                logger.warning(f"Stderr: {result.stderr}")
            
            return result
            
        except subprocess.TimeoutExpired:
            logger.error("Savile Row command timed out")
            return None
        except Exception as e:
            logger.error(f"Failed to run Savile Row: {e}")
            return None
    
    def capture_terminal_screenshot(self, region=None):
        """Capture screenshot of terminal area"""
        try:
            if region:
                # Capture specific region (left, top, width, height)
                screenshot = ImageGrab.grab(bbox=region)
            else:
                # Capture entire screen
                screenshot = ImageGrab.grab()
            
            logger.info("Screenshot captured")
            return screenshot
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")
            return None
    
    def extract_text_from_image(self, image):
        """Extract text from image using TrOCR"""
        try:
            # Convert PIL image to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Process image with TrOCR
            pixel_values = self.trocr_processor(image, return_tensors="pt").pixel_values
            generated_ids = self.trocr_model.generate(pixel_values)
            generated_text = self.trocr_processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            
            logger.info(f"Extracted text: {generated_text[:100]}...")
            return generated_text
            
        except Exception as e:
            logger.error(f"Failed to extract text from image: {e}")
            return None
    
    def write_output_file(self, content, filename="output.txt"):
        """Write content to output file"""
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(content)
            logger.info(f"Written output to {filename}")
        except Exception as e:
            logger.error(f"Failed to write output file: {e}")
    
    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()
            logger.info("Selenium driver closed")
    
    def run_automation(self, click_coords=None, essence_file="essence.eprime", param_file="param.param"):
        """Main automation workflow"""
        try:
            logger.info("Starting Savile Row automation...")
            
            # Step 1: Setup Selenium
            self.setup_selenium()
            
            # Step 2: Perform manual clicks if coordinates provided
            if click_coords:
                for coord in click_coords:
                    if len(coord) == 3:  # (x, y, double_click)
                        self.click_screen(coord[0], coord[1], coord[2])
                    else:  # (x, y)
                        self.click_screen(coord[0], coord[1])
            
            # Step 3: Read essence and parameter files
            essence_content = self.read_file_contents(essence_file)
            param_content = self.read_file_contents(param_file)
            
            if not essence_content or not param_content:
                logger.error("Failed to read required files")
                return False
            
            # Step 4: Run Savile Row
            result = self.run_savillerow(essence_file, param_file)
            
            if not result:
                logger.error("Savile Row execution failed")
                return False
            
            # Step 5: Capture terminal screenshot
            # You may need to adjust these coordinates based on your terminal position
            terminal_region = (0, 0, 1920, 1080)  # Adjust as needed
            screenshot = self.capture_terminal_screenshot(terminal_region)
            
            if not screenshot:
                logger.error("Failed to capture terminal screenshot")
                return False
            
            # Step 6: Extract text from screenshot
            extracted_text = self.extract_text_from_image(screenshot)
            
            if not extracted_text:
                logger.error("Failed to extract text from screenshot")
                return False
            
            # Step 7: Combine all output information
            output_content = f"""
=== SAVILE ROW AUTOMATION RESULTS ===

=== ESSENCE FILE CONTENT ===
{essence_content}

=== PARAMETER FILE CONTENT ===
{param_content}

=== SAVILE ROW OUTPUT ===
Return Code: {result.returncode}
Stdout: {result.stdout}
Stderr: {result.stderr}

=== TERMINAL TEXT (OCR) ===
{extracted_text}

=== END OF RESULTS ===
"""
            
            # Step 8: Write output file
            self.write_output_file(output_content)
            
            logger.info("Automation completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Automation failed: {e}")
            return False
        finally:
            self.cleanup()

def main():
    """Main function to run the automation"""
    
    # Configuration
    SAVILLEROW_PATH = "./savillerow"  # Adjust path as needed
    ESSENCE_FILE = "essence.eprime"
    PARAM_FILE = "param.param"
    
    # Optional: Define click coordinates (x, y) or (x, y, double_click_bool)
    # Example: [(100, 200), (300, 400, True)]  # Second click is double-click
    CLICK_COORDINATES = [
        # (500, 300),        # Single click at (500, 300)
        # (600, 400, True),  # Double click at (600, 400)
    ]
    
    # Create and run automation
    automation = SavilleRowAutomation(SAVILLEROW_PATH)
    
    try:
        success = automation.run_automation(
            click_coords=CLICK_COORDINATES,
            essence_file=ESSENCE_FILE,
            param_file=PARAM_FILE
        )
        
        if success:
            print("Automation completed successfully! Check output.txt for results.")
        else:
            print("Automation failed. Check logs for details.")
            
    except KeyboardInterrupt:
        logger.info("Automation interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        automation.cleanup()

if __name__ == "__main__":
    main()

    # runanti savillerow u linuxu sa pythonom
    