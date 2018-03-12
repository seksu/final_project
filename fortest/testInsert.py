#created by sek su
from datetime import datetime
import MySQLdb

fileName        = "a12120180222114235.avi"

dt_str          = fileName[10:12]+'/'+fileName[8:10]+'/'+fileName[4:8]+' '+fileName[12:14]+':'+fileName[14:16]+':'+fileName[16:18]
timestamp       = datetime.strptime(dt_str, '%d/%m/%Y %I:%M:%S')
recognition_face= None
face_path       = "face/a121201802221142350.jpg"
fullbody_path   = "body/a121201802221142350.jpg"
videopath       = "video/a12120180222114235.avi"
timelapse       = 30
position_x      = 240
position_y      = 250
position_w      = 260
position_h      = 270
shirtcolor_r    = 255
shirtcolor_g    = 128
shirtcolor_b    = 0
account         = None

# Open database connection
db = MySQLdb.connect("localhost","root","654321","faces" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.
sql = "INSERT INTO source_searching_detail(timestamp,recognition_face,face_path,\
        fullbody_path,videopath,timelapse,position_x,position_y,position_w,position_h,\
        shirtcolor_r,shirtcolor_g,shirtcolor_b,account) VALUES ('%Y', '%s', '%s', '%s',\
        '%s', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d')" % (timestamp,recognition_face,\
        face_path,fullbody_path,videopath,timelapse,position_x,position_y,position_w,pos_body_h,\
        shirtcolor_r,shirtcolor_g,shirtcolor_b,account)
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Commit your changes in the database
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()
# disconnect from server
db.close()
