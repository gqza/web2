import os
from datetime import datetime

# Configuration
FOLDER_PATH = 'pages'                  
RSS_OUTPUT_PATH = 'public/rss.xml'     
BASE_URL = 'https://iilwy.nekoweb.org/'

IGNORE_LIST = [
    'rss.xml',
    'archive',
    '404.md',
    'index.md',
    'new.md'
]


file_data_list = []

if os.path.exists(FOLDER_PATH):
    for root, dirs, files in os.walk(FOLDER_PATH):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for filename in files:
            if filename.startswith('.') or filename in IGNORE_LIST:
                continue
                
            file_path = os.path.join(root, filename)
            
            rel_path = os.path.relpath(file_path, FOLDER_PATH).replace('\\', '/')
            
            page_slug = rel_path
            if page_slug.lower().endswith('.md'):
                page_slug = page_slug[:-3]
            
            # Format URL to pass the filename into your query parameter route
            file_url = f"{BASE_URL}?{page_slug}"
            
            m_time = os.path.getmtime(file_path)
            pub_date = datetime.utcfromtimestamp(m_time).strftime('%a, %d %b %Y %H:%M:%S GMT')
            
            file_data_list.append({
                'm_time': m_time,
                'title': page_slug.replace('/', ' ➔ '), # Clean up title display for subfolders
                'file_url': file_url,
                'pub_date': pub_date
            })

file_data_list.sort(key=lambda x: x['m_time'], reverse=True)

latest_items = file_data_list[:20]

rss_items = []
for item in latest_items:
    rss_items.append(f"""
        <item>
            <title>{item['title']}</title>
            <link>{item['file_url']}</link>
            <guid>{item['file_url']}</guid>
            <pubDate>{item['pub_date']}</pubDate>
        </item>""")

rss_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
    <title>iilwy.nekoweb.org Updates</title>
    <link>{BASE_URL}</link>
    <description>Zavi's RSS brought to you by github actions :D</description>
    <language>en-us</language>
    {"".join(rss_items)}
</channel>
</rss>
"""

os.makedirs(os.path.dirname(RSS_OUTPUT_PATH), exist_ok=True)

with open(RSS_OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write(rss_content)
print(f"RSS feed successfully generated for custom router at {RSS_OUTPUT_PATH}")