#!/usr/bin/env python3
import datetime
import sys
import os
import cqupt_ics
import providers
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

def generate_stream_response(gen, first_event: str):
	if first_event != None:
		yield cqupt_ics.ICS_HEADER
		yield first_event
		for event in gen:
			yield event
		yield cqupt_ics.ICS_FOOTER
	else:
		yield ''

@app.route("/<int:stu_id>.ics", methods=['GET'])
def respond_ics(stu_id: int):
	with_class = bool(int(request.args.get('class', True)))
	with_exam = bool(int(request.args.get('exam', True)))
	with_geo = bool(int(request.args.get('geo', True)))
	provider_name = request.args.get('provider', None)
	err = None

	provider_list = []
	try:
		if provider_name:
			provider_list.append(providers.providers[provider_name])
		else:
			for key in providers.providers:
				provider_list.append(providers.providers[key])
	except:
		return Response(status=400, response="请求了无效的数据源")

	for provider in provider_list:
		provider: providers.ProviderBaseType
		try:
			gen = cqupt_ics.get_events(student_id=stu_id, 
						mode=((with_exam * cqupt_ics.ICS_EXAM) | (with_class * cqupt_ics.ICS_CLASS)), 
						enable_geo=with_geo, 
						provider=provider,
						start_day=START_DAY)
			first_val = next(gen, None)
			return Response(response=generate_stream_response(gen, first_val), mimetype="application/octet-stream")
		except Exception as e:
			err = e
	return Response(status=503, response=err.args[0])

def main(argv=[]):
	app.run(host="0.0.0.0", port=PORT)

if __name__ == "__main__":
	main(sys.argv)