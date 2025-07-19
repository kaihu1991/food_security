from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import re
import unicodedata


# Get configured driver example
def get_undetected_chrome_driver():
    options = Options()
    # Create a Chrome options object to customize browser settings.
    options.add_argument("--disable-blink-features=AutomationControlled")
    # Disable the "AutomationControlled" Blink feature to help avoid detection.
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # Exclude automation switch to avoid browser notification.
    options.add_experimental_option('useAutomationExtension', False)
    # Disable automation extension.

    driver = webdriver.Chrome(options=options)
    # Execute JavaScript to override the value of window.navigator.webdriver
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""
    })
    return driver


def get_basic_data(every_url):
    driver = get_undetected_chrome_driver()
    result_basic_df = pd.DataFrame(columns=["姓名", "性别", "籍贯", "出生日期", "毕业院校", "政治面貌", "学历","网址"])
    # Create an empty DataFrame with predefined column names for storing personal profile information.
    for url in tqdm(every_url):  # 获取信息
        if url == "None" or pd.isna(url):
            # Check if the URL is the string "None" or a missing (NaN) value.

            print(url)
            print("None")
            city_data = pd.DataFrame({"姓名": [""], "性别": [""], "籍贯": [""],
                                      "出生日期": [""], "毕业院校": [""], "政治面貌": [""], "学历": [""], "网址": [""]})
            result_basic_df = pd.concat([result_basic_df, city_data], ignore_index=True)
            continue
        try:
            every = {}
            driver.get(url)
            time.sleep(2)
            if "验证" in driver.page_source or "请输入验证码" in driver.page_source:
                input("⚠️ 检测到验证，请手动处理验证后按回车继续...")
                # Check if the page contains a verification prompt (e.g., CAPTCHA);
                # pause execution and wait for manual completion.

            html = driver.page_source
            # Retrieve the HTML source code of the current page.

            soup = BeautifulSoup(html, 'html.parser')
            mag_source = soup.find_all('div', class_="basicInfo_Dxt9K J-basic-info")
            # Try to find the container div with the primary class used for basic personal information.

            if not mag_source:
                mag_source = soup.find_all('div', class_="basicInfo_v5QUh J-basic-info")
                # If not found, try with an alternative class name (due to possible page layout variations).

                if not mag_source:
                    mag_source = soup.find_all('div', class_="basicInfo_GEyLT J-basic-info")
                    # Try a third variation of the class name.

                    if not mag_source:
                        print(url)
                        city_data = pd.DataFrame({"姓名": [""], "性别": [""], "籍贯": [""],
                                                  "出生日期": [""], "毕业院校": [""], "政治面貌": [""], "学历": [""], "网址": [""]})
                        # Create an empty row with blank values to maintain data structure consistency.

                        result_basic_df = pd.concat([result_basic_df, city_data], ignore_index=True)
                        # Append the empty row to the result DataFrame.

                        continue
                        # Skip to the next URL or iteration.

            dd_tags = mag_source[0].find_all('dd')
            # Find all <dd> tags, which contain the values (e.g., birthplace, education).

            dt_tags = mag_source[0].find_all('dt')
            # Find all <dt> tags, which are the field labels (e.g., "Birthplace", "Education").

            for index, dt in enumerate(dt_tags):
                clean_text = unicodedata.normalize("NFKC", dt.text)
                # Normalize unicode characters to standard form (e.g., convert full-width to half-width).

                clean_text = clean_text.replace(" ", "")
                # Remove all spaces from the label text.

                clean_text = clean_text.strip()
                # Remove any leading or trailing whitespace.

                every[clean_text.replace('\xa0', '')] = dd_tags[index].text.replace('\xa0', '')
                # Clean the key and value text and store them in a dictionary called 'every'.

        except Exception as e:
            city_data = pd.DataFrame({"姓名": [""], "性别": [""], "籍贯": [""],
                                      "出生日期": [""], "毕业院校": [""], "政治面貌": [""], "学历": [""], "网址": [""]})
            result_basic_df = pd.concat([result_basic_df, city_data], ignore_index=True)
            print(url)
            continue
        city_data = pd.DataFrame(
            {"姓名": [every.get("中文名", "")], "性别": [every.get("性别", "")],
             "籍贯": [every.get("籍贯", every.get("出生地", ""))], "出生日期": [every.get("出生日期", "")],
             "毕业院校": [every.get("毕业院校", "")], "政治面貌": [every.get("政治面貌", "")],
             "学历": [every.get("学历", "")], "网址": [url]})
        result_basic_df = pd.concat([result_basic_df, city_data], ignore_index=True)
    return result_basic_df


def get_lvli_data(every_url,every_name):
    driver = get_undetected_chrome_driver()
    result_lvli_df = pd.DataFrame(columns=["姓名", "基本信息","履历", "网址"])
    for index, url in enumerate(tqdm(every_url)):
        if url == "None" or pd.isna(url):
            city_data = pd.DataFrame({"姓名": [''], "基本信息": [''], "履历": [''], "网址": ''})
            result_lvli_df = pd.concat([result_lvli_df, city_data], ignore_index=True)
            continue
        try:
            city_info = []
            driver.get(url)
            time.sleep(2)
            if "验证" in driver.page_source or "请输入验证码" in driver.page_source:
                input("⚠️ 检测到验证，请手动处理验证后按回车继续...")
            # Check if the page contains a verification prompt (e.g., CAPTCHA);
            # pause execution and wait for manual completion.

            html = driver.page_source
            # Retrieve the HTML source code of the current page.

            soup1 = BeautifulSoup(html, 'html.parser')
            meta_tag = soup1.find('meta', {'name': 'description'})
            items2 = meta_tag.get('content')
            items3 = soup1.find_all('div', class_="para_fT72O content_pzMvr MARK_MODULE")
            # Try to find the container div with the primary class used for basic personal information.

            if not items3:
                items3 = soup1.find_all('div', class_="para_jzmEb content_BNj1q MARK_MODULE")
                if not items3:
                    print(url)
                    city_data = pd.DataFrame(
                        {"姓名": [every_name[index]], "基本信息": [items2], "履历": [""], "网址": [url]})
                    result_lvli_df = pd.concat([result_lvli_df, city_data], ignore_index=True)
                    # Create an empty row with blank values to maintain data structure consistency.

                    continue
            for item3 in items3:
                # if info_city1 in item3.get_text():
                cleaned_text = (re.sub(r'\[[^]]*]', '', item3.get_text())).split('\n')
                # Remove reference-like patterns (e.g., [1], [2]) using regex and split the text by newlines.

                cleaned_city = '\n'.join(line.strip() for line in cleaned_text if line.strip())
                # Strip leading/trailing whitespace from each line and remove empty lines, then join them back.

                city_info.append(cleaned_city)
                city_info_str = '\n'.join(city_info)
            # print("爬取成功")
            city_data = pd.DataFrame({"姓名": [every_name[index]], "基本信息": items2, "履历": [city_info_str], "网址": [url]})
            result_lvli_df = pd.concat([result_lvli_df, city_data], ignore_index=True)
        except Exception as e:
            print(f"爬取 {every_name[index]} 市委书记信息出现错误：{str(e)}")
            city_data = pd.DataFrame({"姓名": [every_name[index]], "基本信息": [''], "履历": [''], "网址": url})
            result_lvli_df = pd.concat([result_lvli_df, city_data], ignore_index=True)
            continue
    return result_lvli_df


df = pd.read_excel('../resource/secretary_url.xlsx')


every_url = df['网址']
every_name = df['姓名']


result_basic_df = get_basic_data(every_url)
result_lvli_df = get_lvli_data(every_url,every_name)

# Horizontally concatenate two DataFrames, ignoring duplicate column names
merged_df = pd.concat([result_basic_df, result_lvli_df], axis=1)

# Remove duplicate columns, keeping only the first occurrence
merged_df = merged_df.loc[:, ~merged_df.columns.duplicated()]

# Define the desired column order
desired_order = ["姓名", "基本信息","履历","籍贯", "出生日期","毕业院校","政治面貌","学历","网址"]

# Reorder the columns in the desired sequence
merged_df = merged_df[desired_order]

# Store the saved data in this file
merged_df.to_excel("../output/secretary_data.xlsx", index=False)





