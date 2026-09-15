import os
from datetime import datetime, UTC
from itertools import islice

FOLDER_PATH = './public/pages'                  
RSS_OUTPUT_PATH = './public/rss.xml'     
BASE_URL = 'https://iilwy.nekoweb.org'

IGNORE_LIST = [
    'rss.xml',
    '404.md',
    'index.md',
    'new.md',
    'archive',
    'archive.md'
]

file_data_list = []

if os.path.exists(FOLDER_PATH):
    for root, dirs, files in os.walk(FOLDER_PATH):
        dirs[:] = [d for d in dirs if d not in IGNORE_LIST and not d.startswith('.')]
        
        for filename in files:
            if filename.startswith('.') or filename in IGNORE_LIST:
                continue
                
            file_path = os.path.join(root, filename)
            
            description = "No description available"
            if filename.lower().endswith('.md'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        third_line_list = list(islice(f, 2, 3))
                        if third_line_list:
                            description = third_line_list[0].strip()
                except Exception:
                    pass
            
            rel_path = os.path.relpath(file_path, FOLDER_PATH).replace('\\', '/')
            
            page_slug = rel_path
            if page_slug.lower().endswith('.md'):
                page_slug = page_slug[:-3]
            
            file_url = f"{BASE_URL}?{page_slug}"
            
            m_time = os.path.getmtime(file_path)
            pub_date = datetime.fromtimestamp(m_time, UTC).strftime('%a, %d %b %Y %H:%M:%S GMT')
            
            file_data_list.append({
                'm_time': m_time,
                'title': page_slug.replace('/', ' ➔ '),
                'file_url': file_url,
                'pub_date': pub_date,
                'description': description
            })
else:
    print(f"Error: The directory '{FOLDER_PATH}' could not be found!")

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
            <description>
                <![CDATA[
                    <p>{item['description']}</p>
                    <p>Read the rest at <a href="iilwy.nekoweb.org">iilwy.nekoweb.org</a></p>
                ]]>
            </description>
        </item>""")

first_item_desc = latest_items[0]['description'] if latest_items else "No description available"
first_item_url = latest_items[0]['file_url'] if latest_items else BASE_URL
first_item_date = latest_items[0]['pub_date'] if latest_items else datetime.now(UTC).strftime('%a, %d %b %Y %H:%M:%S GMT')

rss_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
    <atom:link href="{BASE_URL}/rss.xml" rel="self" type="application/rss+xml" />
    <title>zavi</title>
    <link>{BASE_URL}</link>
    <description>Zavi's RSS brought to you by github actions :D</description>
    <language>en-us</language>
    <item>
            <title>PINNED</title>
            <link>{BASE_URL}</link>
            <guid>{BASE_URL}</guid>
            <pubDate>{first_item_date}</pubDate>
            <description>If you're reading this, you've subscribed to the RSS feed. Chances are it will randomly inundate you with "new" posts. I apologize in advance.
            
            - zavi</description>
        </item>
    {"".join(rss_items)}
</channel>
</rss>
"""

os.makedirs(os.path.dirname(RSS_OUTPUT_PATH), exist_ok=True)

with open(RSS_OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write(rss_content)
print(f"RSS feed successfully generated for custom router at {RSS_OUTPUT_PATH}")
