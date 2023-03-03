import os
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

def wordpress_to_markdown(post):
    lines = post.replace('\r','').split("\n")
    ret = []
    for line in lines:
        line = line.replace('<p class="p1">', '\n')
        if line.startswith("<strong>"):
            line = line.replace('<strong>','# ')
        line = line.replace('</p>', '\n')
        line = line.replace('</strong>', '')
        ret.append(line)
    ret = "\n".join(ret)
    ret = ret + "\n"
    return ret

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
