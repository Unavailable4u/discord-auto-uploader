import os
import time
from tkinter import Tk
from tkinter.filedialog import askdirectory
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ========================= CONFIG =========================
DISCORD_URL = "https://discord.com/channels/@me"

UPLOAD_SELECTORS = [
    'button[aria-label="Upload a file"]',
    'div[aria-label="Upload a file"]',
    'button svg[viewBox="0 0 24 24"]',
    '.attachButtonPlus__0923f',
    'button[class*="attachButton"]'
]

FILE_INPUT_SELECTOR = 'input[type="file"]'
MESSAGE_BOX_SELECTOR = 'div[role="textbox"]'

BATCH_SIZE = 10
DELAY_BETWEEN_BATCHES = 7
CUSTOM_MESSAGE = ""  # Leave empty or put your message here
# ========================================================

def choose_sorting():
    """Let user choose sorting method"""
    print("\n" + "="*50)
    print("🎯 Choose Sorting Method:")
    print("="*50)
    print("1. Name (Filename)")
    print("2. Date Modified")
    print("3. Size")
    print("="*50)
    
    while True:
        try:
            choice = int(input("\nEnter your choice (1-3): "))
            if choice in [1, 2, 3]:
                break
            print("Please enter 1, 2 or 3.")
        except:
            print("Invalid input. Please enter a number.")

    order = input("Ascending or Descending? (A/D): ").strip().lower()
    reverse = order == 'd'
    
    if choice == 1:
        sort_type = "Name"
    elif choice == 2:
        sort_type = "Date Modified"
    else:
        sort_type = "Size"
    
    print(f"✅ Selected: {sort_type} {'Descending' if reverse else 'Ascending'}")
    return choice, reverse

def get_files(folder, sort_choice=1, reverse=False):
    file_list = []
    for f in os.listdir(folder):
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.mp4', '.webm', '.mov')):
            full_path = os.path.join(folder, f)
            try:
                if sort_choice == 2:   # Date Modified
                    key = os.path.getmtime(full_path)
                elif sort_choice == 3: # Size
                    key = os.path.getsize(full_path)
                else:                  # Name (default)
                    key = f.lower()
                file_list.append((full_path, key))
            except:
                file_list.append((full_path, 0))
    
    # Sort the files
    file_list.sort(key=lambda x: x[1], reverse=reverse)
    return [item[0] for item in file_list]

def close_all_popups(driver):
    try:
        driver.execute_script("""
            document.querySelectorAll('[aria-label="Inbox"], [class*="inbox"], [role="dialog"], .modal, .layer').forEach(el => {
                const text = (el.innerText || '').toLowerCase();
                if (text.includes('inbox') || text.includes('microphone') || text.includes('allow')) {
                    el.style.display = 'none';
                    el.remove();
                }
            });
            document.querySelectorAll('button[aria-label*="Close"], button[class*="close"]').forEach(btn => {
                try { btn.click(); } catch(e){}
            });
        """)
    except:
        pass

def wait_for_upload_complete(driver, timeout=30):
    print("⏳ Waiting for upload to complete...")
    start = time.time()
    while time.time() - start < timeout:
        try:
            progress = driver.execute_script("""
                return document.querySelectorAll('div[role="progressbar"], .uploadProgress, [class*="progress"]').length;
            """)
            if progress == 0:
                time.sleep(1.5)
                return True
        except:
            pass
        time.sleep(1.2)
    return False

def upload_batch(driver, file_paths, batch_number, total_batches, total_files):
    try:
        print(f"\n🔄 Batch {batch_number}/{total_batches} → {len(file_paths)} files")

        close_all_popups(driver)

        for selector in UPLOAD_SELECTORS:
            try:
                btn = WebDriverWait(driver, 8).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                btn.click()
                print("✅ Upload button clicked")
                break
            except:
                continue
        else:
            raise Exception("Upload button not found")

        time.sleep(1.2)

        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, FILE_INPUT_SELECTOR))
        )
        file_input.send_keys('\n'.join(file_paths))

        wait_for_upload_complete(driver)
        close_all_popups(driver)

        if CUSTOM_MESSAGE.strip():
            try:
                msg_box = WebDriverWait(driver, 6).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, MESSAGE_BOX_SELECTOR))
                )
                msg_box.send_keys(CUSTOM_MESSAGE)
                time.sleep(0.7)
            except:
                pass

        ActionChains(driver).send_keys(Keys.ENTER).perform()
        time.sleep(0.8)

        print(f"✅ Batch {batch_number} Sent Successfully")
        time.sleep(DELAY_BETWEEN_BATCHES)
        return True

    except Exception as e:
        print(f"❌ Batch {batch_number} Failed: {e}")
        time.sleep(5)
        return False

# ===================== MAIN =====================
print("Select the folder containing your media...")
Tk().withdraw()
folder_path = askdirectory()

if not folder_path:
    print("No folder selected.")
    exit()

# === Sorting Choice ===
sort_choice, reverse = choose_sorting()

files = get_files(folder_path, sort_choice, reverse)
total_files = len(files)
print(f"Found {total_files} media files. Ready to upload.")

if total_files == 0:
    print("No supported files found!")
    exit()

# ================== CHROME OPTIONS ==================
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--use-fake-ui-for-media-stream")
options.add_argument("--use-fake-device-for-media-stream")

prefs = {
    "profile.default_content_setting_values.media_stream_mic": 2,
    "profile.default_content_setting_values.media_stream_camera": 2,
    "profile.default_content_setting_values.notifications": 2,
}
options.add_experimental_option("prefs", prefs)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(DISCORD_URL)

print("\n" + "="*60)
print("1. Login if needed")
print("2. Go to your target channel")
print("3. Click once inside the message input box")
print("="*60)

input("\nPress Enter when you are READY to start uploading...")

close_all_popups(driver)
time.sleep(2)

# Start Uploading
total_batches = (total_files + BATCH_SIZE - 1) // BATCH_SIZE
successful = 0

for i in range(0, total_files, BATCH_SIZE):
    batch = files[i:i + BATCH_SIZE]
    batch_number = (i // BATCH_SIZE) + 1
    if upload_batch(driver, batch, batch_number, total_batches, total_files):
        successful += 1

print(f"\n🎉 Finished! {successful}/{total_batches} batches completed.")
input("\nPress Enter to close the browser...")
driver.quit()