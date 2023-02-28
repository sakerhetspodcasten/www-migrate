import sqlite3

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
        print(a)

def main():
    con = get_connection()
    load_schema(con)
    truncate_posts(con)
    load_posts(con)
    export_posts(con)

if __name__ == "__main__":
    main()
