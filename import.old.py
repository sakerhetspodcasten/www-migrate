import sqlite3

def get_connection():
    con = sqlite3.connect(".legacy/sqllite.db")
    return con

def load_schema(con):
    with open('.legacy/schema.sql') as f:
        lines = [line.rstrip("\r ") for line in f]
    schema_sql = "\n".join(lines)
    cur = con.cursor()
    con.execute(schema_sql)

def load_posts(con):
    with open('.legacy/posts.sql') as f:
        lines = [line.rstrip("\r\n ") for line in f]
    
    #raise Exception(len(lines))

    posts_sql = ""
    for line in lines:
        print(f"line: [ {line} ]")
        posts_sql = posts_sql + line
        if line.endswith(");"):
            posts_sql = posts_sql.replace("\\\"", "\"\"")
            print(f"posts_sql: [ {posts_sql} ]")
            cur = con.cursor()
            con.execute(posts_sql)
            posts_sql = ""
        else:
            posts_sql = posts_sql + "\n"
    if posts_sql != "":
        raise Exception(f"Expected last string empty, got [ {posts_sql} ]")


def main():
    con = get_connection()
    load_schema(con)
    load_posts(con)

if __name__ == "__main__":
    main()
