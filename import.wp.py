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


def main():
    con = get_connection()
    load_schema(con)
    truncate_posts(con)
    load_posts(con)

if __name__ == "__main__":
    main()
