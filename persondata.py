import MySQLdb

class DataImport():
  def get_data(self):
    conn = MySQLdb.connect(host="72.52.77.158", port=8080, user="project42", passwd="startupweekend",db="project42")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM w2m_user")
    rows = cursor.fetchall()
    cursor.close()
    return rows
