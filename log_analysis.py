#!/usr/bin/python3


import psycopg2


DBNAME = "news"


# Define a function to take in the SQL query and return its result
def run_query(query):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results


# Query that answers 'what are the most popular 3 articles of all time?'
query_1 = (
    "select articles.title, count(log.path) as views "
    "from articles join log on log.path like concat('%', articles.slug) "
    "where log.status like '%OK%' "
    "group by log.path, articles.title "
    "order by views desc "
    "limit 3"
    )


# Query that answers 'Who are the most popular article authors of all time?'
query_2 = (
    "select authors.name, count(log.path) as views "
    "from authors join articles on authors.id = articles.author "
    "join log on log.path like concat('%', articles.slug) "
    "where log.status like '%OK%' "
    "group by authors.name, log.path "
    "order by views desc "
    "limit 1"
    )

# Query to answer 'On which days did more than 1% of requests lead to errors?'
query_3 = (
    "select * from ("
    "select substring(cast(log.time as text), 0, 11) as day, "
    "round(sum(case log.status when '200 OK' then "
    "0 else 1 end)*100.0/count(log.status),2) as err_pct "
    "from log "
    "group by day) as base "
    "where err_pct >= 1 "
    "order by err_pct desc"
    )


# Function to print the result of 1st and 2nd question in a better format
def print_result(phrase, answer):
    print(phrase)
    for each in answer:
        print(each[0], "---", each[1], "views")


# Function to print the result to the third question in a better format
def print_err_result(phrase, answer):
    print(phrase)
    for each in answer:
        print(each[0], "---", each[1], "%")


# print the outputs to the reader
if __name__ == '__main__':
    print_result("The 3 most popular articles are ", run_query(query_1))
    print_result("The most popular author of all time is ", run_query(query_2))
    print_err_result("The days more than 1% of requests "
                     "lead to errors are ", run_query(query_3))
