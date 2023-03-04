import datetime
import feedparser
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

def process_entry(e):
    title        = e['title']
    published_p  = e['published_parsed']
    summary      = e['summary']
    content      = e['content']
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
    header={}
    header['title'] = title
    header['date'] = published_pp
    header_yaml = yaml.dump(header)
    print("---")
    print("## Lyssna")
    print(f"* [mp3]({mp3}), längd: {duration}") 
    print("## Innehåll")
    print(summary)

def main():
    rss = load_rss()
    entries = rss['entries'];
    for entry in entries:
        process_entry(entry)

if __name__ == "__main__":
    main()
