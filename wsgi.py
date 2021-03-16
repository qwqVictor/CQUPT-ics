#!/usr/bin/env python3
import datetime
import sys
import os
import cqupt_ics
from flask import Flask, request, Response
from urllib.parse import unquote

try:
	START_DAY_STR = os.getenv("START_DAY") if os.getenv("START_DAY") else "1970-01-01"
	PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 3000
except:
	START_DAY_STR = "1970-01-01"
	PORT = 3000

start_day_tuple = ()
for i in START_DAY_STR.split('-'):
	start_day_tuple += (int(i),)

START_DAY = datetime.datetime(start_day_tuple[0], start_day_tuple[1], start_day_tuple[2])

app = Flask(__name__)

@app.route("/<int:stu_id>.ics", methods=['GET'])
def respond_ics(stu_id: int):
	with_class= bool(int(request.args.get('class', True)))
	with_exam = bool(int(request.args.get('exam', True)))
	with_geo= bool(int(request.args.get('geo', True)))

	data = cqupt_ics.get_ics(student_id=stu_id, 
						mode=((with_exam * cqupt_ics.ICS_EXAM) | (with_class * cqupt_ics.ICS_CLASS)), 
						enable_geo=with_geo, 
						start_day=START_DAY)
	if data:
		return Response(response=data, mimetype="application/octet-stream")
	else:
		return Response(status=400, response="Bad Request")

def main(argv=[]):
	app.run(host="0.0.0.0", port=PORT)

if __name__ == "__main__":
	main(sys.argv)