import os
import re
import sqlite3
import yaml

def get_connection():
    con = sqlite3.connect("wp-legacy/sqllite.db")
    return con

def load_schema(con):
    with open('wp-legacy/posts.schema') as f:
        lines = [line.rstrip("\r ") for line in f]
    schema_sql = "\n".join(lines)
    cur = con.cursor()
    con.execute(schema_sql)

def truncate_posts(con):
    cur = con.cursor()
    con.execute("DELETE FROM wp_posts")

def load_posts(con):
    with open('wp-legacy/posts.sql') as f:
        lines = [line.rstrip("\r\n ") for line in f]
    
    posts_sql = ""
    line_count = 0
    inserts = 0
    for line in lines:
        #print(f"line: [ {line} ]")
        posts_sql = posts_sql + line
        if line.endswith(");"):
            posts_sql = posts_sql.replace("\\\"", "\"\"")
            #print(f"posts_sql: [ {posts_sql} ]")
            #print(f"Execute SQL, {line_count} line(s).")
            cur = con.cursor()
            con.execute(posts_sql)
            inserts = inserts + 1
            line_count = 0
            posts_sql = ""
        else:
            line_count = line_count + 1
            posts_sql = posts_sql + "\n"
    print(f"load_posts(): executed {inserts} statement(s)")
    if posts_sql != "":
        raise Exception(f"Expected last string empty, got [ {posts_sql} ]")

def row_to_dict(column_names, row):
    column_count = len(column_names)
    data = {}
    for i in range(column_count):
        cn = column_names[i]
        cd = row[i]
        data[cn] = cd
    return data

def prune_rows_to_awesome_dict(column_names, rows):
    awesome = {}
    for row in rows:
        d = row_to_dict(column_names, row)
        pid     = d["ID"]
        pparent = d["post_parent"]
        ptype   = d["post_type"]

        if ptype == "attachment":
            continue
        elif ptype == "revision":
            if pparent not in awesome.keys():
                awesome[pparent] = d
        else:
            if pid not in awesome.keys():
                awesome[pid] = d
            else:
                awesome[pid]["ID"] = pid
                awesome[pid]["post_type"] = ptype
    return awesome

def mkdir(p):
    if not os.path.exists(p):
        os.makedirs(p)

def date_format_with_tea( boring_date ):
    tea = boring_date.replace(' ', 'T')
    return tea

def append_short_lines(out, line):
    if len(line) < 100:
        out.append(line)
        return
    if " " not in line:
        out.append(line)
        return
    a=None
    b=None
    try:
        index = line.index(" ", 80)
    except ValueError as ve:
        out.append(line)
        return
    a = line[:index].strip(' ')
    b = line[index:].strip(' ')
    out.append(a)
    append_short_lines(out, b)

def arr_to_str(arr):
    ret = "\n".join(arr)
    ret = ret + "\n"
    return ret

def wordpress_to_markdown(post):
    lines = post\
            .replace('\r','\n')\
            .replace('\n</a>',' </a>')\
            .split("\n")
    reg_junk = re.compile(' (dir|rel|data-saferedirecturl|style|target|title)="[^"]*"')
    reg_em = re.compile('<[/]*em>')
    reg_li = re.compile('<li[^>]*>')
    reg_link = re.compile('<a href="([^"]+)">([^<]+)</a>')
    reg_span = re.compile('<(script|span|style|p|ul|div)[^>]*>')
    ret = []
    for line in lines:
        line = line.replace('|','\\|')
        line = reg_junk.sub('', line)
        line = line.replace('&amp;', '&')
        line = line.strip(' ')
        line = reg_em.sub("__", line)
        line = reg_span.sub("", line)
        line = reg_li.sub("* ", line)
        if line.startswith("<b>"):
            line = line.replace('<b>','## ')
        else:
            line = line.replace('<b>','')
        if line.startswith("<i>"):
            line = line.replace('<i>','> ')
        else:
            line = line.replace('<i>','')
        if line.startswith("<strong>"):
            line = line.replace('<strong>','## ')
        else:
            line = line.replace('<strong>','')
        line = line.replace('<wbr />', '\n')
        line = line.replace('<!-- wp:paragraph -->', '')
        line = line.replace('<!-- /wp:paragraph -->','\n')
        line = line.replace('</b>', '\n')
        line = line.replace('</i>', '\n')
        line = line.replace('</div>', '\n')
        line = line.replace('</li>', '\n')
        line = line.replace('</p>', '\n')
        line = line.replace('</span>', '\n')
        line = line.replace('</script>', '')
        line = line.replace('</strong>', '')
        line = line.replace('</ul>', '\n')
        line = reg_link.sub(r'[\2](\1)', line)
        append_short_lines(ret, line)
    return arr_to_str( ret )

def export_post(post):
    POST_CONT  = post["post_content"]
    POST_DATE  = date_format_with_tea( post["post_date_gmt"] )
    POST_MODI  = date_format_with_tea( post["post_modified_gmt"] )
    POST_NAME  = post["post_name"]
    POST_TITLE = post["post_title"]
    POST_TYPE  = post["post_type"]
    fdir=None
    fname=None
    if POST_TYPE == "post":
        fdir = "../www-hugo/content/posts"
    elif POST_TYPE == "page":
        fdir = "../www-hugo/content/pages"
    else:
        print(f"IGNORED: Unknown type {POST_TYPE}")
        return
    mkdir(fdir)
    fname=POST_NAME + ".md"
    with open(fdir + "/" + fname, "w") as f:
        f.write("---\n")
        header = {}
        header["title"] = POST_TITLE
        header["date"] = POST_DATE
        header["lastmod"] = POST_MODI
        header_yaml = yaml.dump(header)
        f.write(header_yaml)
        f.write("---\n")
        content_markdown = wordpress_to_markdown( POST_CONT )
        f.write(content_markdown)

def export_posts(con):
    query = "SELECT "\
            "ID, "\
            "post_author, "\
            "post_date, "\
            "post_date_gmt, "\
            "post_content, "\
            "post_title, "\
            "post_excerpt, "\
            "post_status, "\
            "post_name, "\
            "post_modified, "\
            "post_modified_gmt, "\
            "post_parent, "\
            "menu_order, "\
            "post_type "\
            "FROM wp_posts ORDER BY post_modified_gmt DESC"
    cur = con.execute(query)
    column_names = [i[0] for i in cur.description]
    rows = cur.fetchall()
    awesome = prune_rows_to_awesome_dict(column_names, rows)

    print(awesome.keys())
    for a in awesome.values():
        if a["post_status"] != "publish":
            continue
        export_post(a)

def main():
    con = get_connection()
    load_schema(con)
    truncate_posts(con)
    load_posts(con)
    export_posts(con)

if __name__ == "__main__":
    main()
