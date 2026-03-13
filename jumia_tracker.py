import pandas as pd
from playwright.sync_api import sync_playwright
import datetime
import time
import os
import random
import re

URLS_FILE = "urls.txt"
HISTORY_FILE = "price_history.csv"
MATRIX_FILE = "my_price_matrix.csv"

def clean_price_morocco(price_text):
    if not price_text: return None
    try:
        clean_str = price_text.replace(',', '.')
        clean_str = re.sub(r'[^\d.]', '', clean_str)
        return float(clean_str)
    except: return None

def get_product_name(page):
    try:
        return page.locator("h1").inner_text().strip()
    except:
        return "Unknown Product"

def main():
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0]
            print("Connected to existing Chrome session!")
        except Exception:
            print("COULD NOT CONNECT! Make sure Chrome is open with '--remote-debugging-port=9222'")
            return

        if not os.path.exists(URLS_FILE):
            print(f"Error: Could not find '{URLS_FILE}'")
            return
            
        with open(URLS_FILE, "r") as f:
            urls = [line.strip() for line in f if line.strip()]

        print(f"Loaded {len(urls)} products.")

        if os.path.exists(HISTORY_FILE):
            history_df = pd.read_csv(HISTORY_FILE)
        else:
            history_df = pd.DataFrame(columns=["date", "url", "name", "price"])

        today_str = datetime.datetime.now().strftime("%Y-%m-%d")

        for url in urls:
            print(f"Checking...", end=" ")
            
            page = None 
            try:
                page = context.new_page()
                page.goto(url, timeout=60000, wait_until='domcontentloaded')
                
                try:
                    page.wait_for_selector('text="Dhs"', timeout=5000)
                except:
                    pass

                name = get_product_name(page)
                price_text = None
                
                try:
                    price_locator = page.locator('div[class*="-fs24"], span[class*="-fs24"]').first
                    if price_locator.is_visible(timeout=2000):
                        price_text = price_locator.inner_text()
                    else:
                        dhs_elements = page.get_by_text("Dhs").all()
                        for el in dhs_elements:
                            if el.is_visible():
                                txt = el.inner_text()
                                if any(char.isdigit() for char in txt) and "livraison" not in txt.lower():
                                    price_text = txt
                                    break
                except: pass

                price = clean_price_morocco(price_text)

                if price:
                    print(f"{name[:25]}... : {price}")
                else:
                    print(f"{name[:25]}... : No Price")
                    
                new_row = pd.DataFrame([{
                    "date": today_str,
                    "url": url,
                    "name": name,
                    "price": price
                }])
                
                history_df = pd.concat([history_df, new_row], ignore_index=True)
                history_df.drop_duplicates(subset=['date', 'url'], keep='last', inplace=True)
                history_df.to_csv(HISTORY_FILE, index=False)
                
            except Exception as e:
                print(f"Error: {e}")
            finally:
                if page:
                    try: page.close()
                    except: pass

            time.sleep(random.uniform(2, 4))

        if not history_df.empty:
            print("\nCreating Matrix File...")
            
            matrix_df = history_df.pivot_table(
                index=['name', 'url'], 
                columns='date', 
                values='price', 
                aggfunc='last'
            )
            
            matrix_df.columns = [f"Price {col}" for col in matrix_df.columns]
            
            matrix_df.to_csv(MATRIX_FILE)
            print(f"Saved to '{MATRIX_FILE}'")

        print("Done.")

if __name__ == "__main__":
    main()