import requests
import json
import pandas as pd

# TikTok Post URL
post_url = 'https://www.tiktok.com/@alwayspilipili/video/7466408960329895186'
post_id = post_url.split('/')[-1]

# Headers
headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.tiktok.com/explore',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
}

comments = []
curs = 0

# Function to fetch TikTok comments
def req(post_id, curs):
    url = f'https://www.tiktok.com/api/comment/list/?WebIdLastTime=1729273214&aid=1988&app_language=en&app_name=tiktok_web&aweme_id={post_id}&browser_language=en-US&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F129.0.0.0%20Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&count=20&cursor={curs}&data_collection_enabled=false&device_id=7427171842932786693&device_platform=web_pc&focus_state=true&from_page=video&history_len=6&is_fullscreen=false&is_page_visible=true&odinId=7427171704705188869&os=windows&priority_region=&referer=&region=CA&screen_height=1080&screen_width=1920&tz_name=Asia%2FTehran&user_is_login=false&webcast_language=en&msToken=U488DBL2ELMV88PxvXu7bOKQJVxuv7LnhKNHsWaOT2uQhpGyj5M-7EmUsXBIS9HbQ_bQ35u3Za-f_hVhHMMYsH-4mxWPeJoUeMhgOHOvQ-IaKb5lr3DlgBIYJXCUc9MCexCHXig1u4a98hVjnec74fs=&X-Bogus=DFSzswVYtfhANH-ltQ2xJbJ92U6T&_signature=_02B4Z6wo000017DRplgAAIDBt3uT.9qT9Zew0aLAAIsv87'
    
    try:
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()  # Check for HTTP errors
        raw_data = response.json()
        print(f'We are on cursor {curs}')
        return raw_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching comments: {e}")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON response")
        return None

# Function to parse and extract comments
def parser(data):
    if data and "comments" in data:
        for cm in data['comments']:
            comment_text = cm.get('text', '')  # Extract 'text' directly
            if comment_text:
                comments.append({"comment": comment_text})
    return data

# Loop to fetch all comments
while True:
    raw_data = req(post_id, curs)
    
    if not raw_data:
        print("No valid data retrieved, stopping...")
        break

    parsed_data = parser(raw_data)

    if parsed_data.get('has_more') == 1:
        curs += 20
        print('Moving to the next cursor...')
    else:
        print('No more comments available.')
        break

# Save JSON File
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(comments, f, ensure_ascii=False, indent=4)

# Convert to DataFrame
df = pd.DataFrame(comments)

# Save as CSV
df.to_csv('output.csv', index=False, encoding='utf-8')

# Save as Excel (✅ Fixed)
df.to_excel('output.xlsx', index=False, engine='openpyxl')

print("\nData has been saved as JSON, CSV, and Excel. Good job Muda! 🚀")
