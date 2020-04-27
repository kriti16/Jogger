from app.database.db import db

def filter_records(app, table_schema, table_name, where_stmt, page, per_page):
	with app.app_context():
		offset = (page-1)*per_page
		sql_stmt = "SELECT %s FROM %s %s ORDER BY date DESC LIMIT %s OFFSET %s" %(table_schema, table_name, where_stmt, per_page, offset)
		# print(sql_stmt)
		rows = db.session().execute(sql_stmt).fetchall()
		sql_stmt = "SELECT COUNT(*) FROM %s %s" %(table_name, where_stmt)
		# print(sql_stmt)
		total_rows = db.session().execute(sql_stmt).fetchall()
		return (rows, total_rows[0][0])

def filter_users(app, table_schema, table_name, where_stmt, page, per_page):
	with app.app_context():
		offset = (page-1)*per_page
		sql_stmt = "SELECT %s FROM %s %s ORDER BY username ASC LIMIT %s OFFSET %s" %(table_schema, table_name, where_stmt, per_page, offset)
		# print(sql_stmt)
		rows = db.session().execute(sql_stmt).fetchall()
		sql_stmt = "SELECT COUNT(*) FROM %s %s" %(table_name, where_stmt)
		# print(sql_stmt)
		total_rows = db.session().execute(sql_stmt).fetchall()
		return (rows, total_rows[0][0])

def filter_delete(app, table_name, where_stmt):
	with app.app_context():
		sql_stmt = "SELECT COUNT(*) FROM %s %s" %(table_name, where_stmt)
		# print(sql_stmt)
		rows = db.session().execute(sql_stmt).fetchall()
		sql_stmt = "DELETE FROM %s %s" %(table_name, where_stmt)
		# print(sql_stmt)
		db.session().execute(sql_stmt)
		db.session().commit()
		return rows[0][0]