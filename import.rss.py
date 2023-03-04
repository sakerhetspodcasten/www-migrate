import datetime
import feedparser
import re
import time
import yaml

def load_rss():
    d = feedparser.parse('./libsyn-legacy/rss')
    return d

def timestruct_to_isoformat(ts):
    t = time.mktime(ts)
    dt = datetime.datetime.fromtimestamp(t)
    iso = dt.isoformat()
    return iso

def gimme_mp3(links):
    yolo=None
    for link in links:
        href = link['href']
        if href.endswith('.mp3'):
            return href
        else:
            yolo = href
    return yolo

def line_break_text(text):
    out=""
    lines = text.split("\n")
    for line in lines:
        if " " not in line:
            out = out + line + "\n"
            continue
        if len(line) < 100:
            out = out + line + "\n"
            continue
        try:
            index = line.index(" ", 80)
        except ValueError as ve:
            out = out + line + "\n"
            continue
        a = line[:index].strip(' ')
        b = line[index:].strip(' ')
        out = out + a + "\n"
        out = out + line_break_text(b)
    return out

def libsyn_to_markdown(text):
    text = re.sub("<[/]*p>", "", text)
    text = re.sub('<a href="([^"]+)">([^<]+)</a>', r"[\2](\1)", text)
    text = line_break_text( text )
    return text

# Extremly specific check for our puproses.
# Older than November 2021, we don't care
def ancient(st):
    value = st.tm_year * 100 + st.tm_mon
    if value <= 202111:
        return True
    return False

def process_entry(e):
    published_p  = e['published_parsed']
    if ancient(published_p):
        return
    title        = e['title']
    summary      = e['summary']
    duration     = e['itunes_duration']
    links        = e['links']
    published_pp  = timestruct_to_isoformat( published_p )
    mp3 = gimme_mp3(links)
    #, 'id', 'guidislink', 'links', 'link', 'image', 'summary', 'summary_detail', 'content', 'itunes_duration', 'itunes_explicit', 'tags', 'subtitle', 'subtitle_detail'])
    #print(f"title:     {title}")
    #print(f"pp:        {published_pp}")
    #print(f"summary:   {summary}")
    #print(f"content:   {content}")
    #print(f"mp3:       {mp3}")
    #print(f"duration:  {duration}")
    print("---")
    header = {}
    header['title'] = title
    header['date'] = published_pp
    header_yaml = yaml.dump(header)
    print(header_yaml)
    print("---")
    print("## Lyssna")
    print(f"* [mp3]({mp3}), längd: {duration}") 
    print()
    print("## Innehåll")
    print(libsyn_to_markdown(summary))

def main():
    rss = load_rss()
    entries = rss['entries'];
    for entry in entries:
        process_entry(entry)

if __name__ == "__main__":
    main()
