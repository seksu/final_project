# import  MySQLdb as my
#
#
# def insert_detail(recognition_face, face_path, fullbody_path, videopath):
#     query = "INSERT INTO source_searching_detail(recognition_face, face_path, fullbody_path, videopath, timestamp)"\
#             "VALUES(%s,%s,%s,%s,%s)"
#     from datetime import datetime
#     args = (recognition_face, face_path, fullbody_path, videopath, datetime.now())
#
#     cursor.execute(query, args)
#
#     if cursor.lastrowid:
#         print('last insert id', cursor.lastrowid)
#     else:
#         print('last insert id not found')
#
#     conn.commit()
#     # data = cursor.execute("""SELECT * FROM source_searching_detail""")
#     # print(data)
#     cursor.close()
#     conn.close()
#
# conn = my.connect(host = "localhost",
#                   user = "root",
#                   passwd = "654321",
#                   db = "faces")
# cursor = conn.cursor()
#
# insert_detail('A Sudden Light','A Sudden Light','A Sudden Light','A Sudden Light')
import sys
sys.path.append('/home/pansek/webserver')
import os
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'webserver.settings'
django.setup()
from source.models import Searching_Detail


search = Searching_Detail.objects.create(
    recognition_face = "panzazaza",
	face_path = "panzaza",
	fullbody_path = "panza",
	videopath = "pan",
	timelapse = "50",
	position_x = "X",
	position_y = "Y",
	position_w = "W",
	position_h = "H",
	shirtcolor_r = 1,
	shirtcolor_g = 2,
	shirtcolor_b = 3
)
search.save()

for search in Searching_Detail.objects.all():
    print(search.face_path)
