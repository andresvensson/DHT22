import sys
sys.path.append(sys.path[0].replace('\\tests', ''))
import Database

print(f"""
**************************
      {__file__}
**************************
""")
db = Database.Database()
db.create_new_database()
db.create_table()
db.describe_table()


print('*'*100)
