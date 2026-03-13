# Jumia Price Tracker 🛒📉

A Python script that tracks product prices on Jumia and automatically generates a clean, side-by-side comparison matrix in Excel/CSV format.

**Why this approach?** Jumia uses strict anti-bot protections (like Cloudflare) that instantly block standard headless scrapers. This script bypasses those protections by connecting to a live, human-launched Google Chrome window via the Chrome DevTools Protocol (CDP). By acting as a "co-pilot" to your real browser, it avoids detection.

## ✨ Features

- **Cloudflare Bypass:** Uses your actual Chrome browser to avoid bot detection.
- **Auto-Cleaning Data:** Automatically removes commas from product names so they don't break CSV formatting.
- **Smart Data Extraction:** Isolates raw numbers from currencies (e.g., converts "12,000.00 Dhs" to pure 12000.00).
- **Matrix Dashboard:** Converts a messy chronological log into a clean, easy-to-read pivot table where dates grow horizontally.

## 🛠️ Prerequisites & Requirements

Before you start, you must have the following installed on your machine:

- **Python 3.7 or higher** 2. **Google Chrome** (The standard desktop browser)
- **Python Libraries:** pandas and playwright

## ⚙️ Installation

**1\. Clone or download this repository** to your local machine.

**2\. Install the required Python packages:**

Open your terminal or command prompt in the project folder and run:

  pip install pandas playwright

## 🚀 Step-by-Step Usage Guide

## Step 1: Set up your Target Links

- In the same folder as the script, create a text file named urls.txt.
- Paste the Jumia product URLs you want to track inside this file (one link per line).
  - _Example:_  
     <https://www.jumia.ma/samsung-galaxy-s23-ultra-12-go-ram-256-go-rom-phantom-black-64723530.html>  
     <https://www.jumia.ma/apple-iphone-13-61-128-go-4-go-ram-minuit-44996221.html>

## Step 2: Open the "Remote Control" Chrome Window (CRUCIAL)

Because of Jumia's security, the script cannot open Chrome on its own. **You must open a special Chrome window first.**

Make sure all normal Chrome windows are closed, then open your terminal/command prompt and run the command for your operating system:

**Windows:**

Win+R then insert:

  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\\selenium\\ChromeProfile"

  _(Note: If your Chrome is installed elsewhere, adjust the path to chrome.exe)_

**Mac:**

  Bash

  /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222 --user-data-dir="~/ChromeProfile"

**Linux:**

  Bash

  google-chrome --remote-debugging-port=9222 --user-data-dir="~/ChromeProfile"

**Note:** This will open a blank Chrome window. **Do not close it.** Keep it open in the background.

## Step 3: Run the Tracker

With your Remote Chrome window open, go back to your terminal, navigate to the folder containing the script, and run:

Bash

python jumia_tracker.py

The script will connect to your open Chrome window, loop through your urls.txt, check every price, and save the data.

## 📂 Output Files

Every time you run the script, it manages two files for you:

- **price_history.csv (The Logbook):**
  - This is your raw, chronological backup. The script just adds new rows to the bottom of this file every time it runs.
- **my_price_matrix.csv (The Dashboard):**
  - This is the file you want to open in Excel! The script automatically pivots the logbook into a clean table format.

**Example output of my_price_matrix.csv:**

| **name**           | **Price 2023-10-01** | **Price 2023-10-02** | **Price 2023-10-03** |
| ------------------ | -------------------- | -------------------- | -------------------- |
| Samsung S23. 256GB | 12000.0              | 12000.0              | **11500.0**          |
| ---                | ---                  | ---                  | ---                  |
| iPhone 13. Red     | 8500.0               | **8200.0**           | 8200.0               |
| ---                | ---                  | ---                  | ---                  |

## ⚠️ Troubleshooting

Error: "COULD NOT CONNECT! Make sure Chrome is open..."

Fix: You didn't complete Step 2 correctly.
Make sure absolutely all Chrome windows are closed (check your task manager if needed) before running the terminal command to open the remote-debugging Chrome.
