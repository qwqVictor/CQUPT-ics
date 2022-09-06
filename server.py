#!/usr/bin/env python3
import datetime
import sys
import logging
import os
import cqupt_ics
import providers
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response, StreamingResponse
from urllib.parse import unquote

START_DAY_STR = os.getenv("START_DAY") if os.getenv(
	"START_DAY") else "1970-01-01"
PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 3000
DEFAULT_PROVIDERS = [providers.providers[name] for name in os.getenv("DEFAULT_PROVIDERS").split(",") if name in providers.providers] \
    if os.getenv("DEFAULT_PROVIDERS") else \
    [providers.providers[name] for name in providers.providers]
DEBUG = bool(os.getenv("DEBUG"))

if len(DEFAULT_PROVIDERS) == 0:
	print("配置的数据源无效！")
	sys.exit(1)
else:
	print("已加载数据源：%s" % DEFAULT_PROVIDERS)

start_day_tuple = ()
for i in START_DAY_STR.split('-'):
	start_day_tuple += (int(i),)

START_DAY = datetime.datetime(
	start_day_tuple[0], start_day_tuple[1], start_day_tuple[2])

app = FastAPI()

async def generate_stream_response(gen, first_val: str):
	if first_val and first_val != '':
		yield cqupt_ics.ICS_HEADER
		yield first_val
	async for event in gen:
		yield event
	yield cqupt_ics.ICS_FOOTER

@app.get("/{stu_id}.ics")
async def respond_ics(stu_id: str, request: Request):
	with_class = bool(int(request.query_params.get('class', True)))
	with_exam = bool(int(request.query_params.get('exam', True)))
	with_geo = bool(int(request.query_params.get('geo', True)))
	provider_name = request.query_params.get('provider', None)
	err = None

	provider_list = []
	try:
		if provider_name:
			provider_list = [providers.providers[provider_name]]
		else:
			provider_list = DEFAULT_PROVIDERS
	except:
		return Response(status_code=400, content="请求了无效的数据源")

	for provider in provider_list:
		provider: providers.ProviderBaseType
		gen = cqupt_ics.get_events(student_id=stu_id,
							mode=((with_exam * cqupt_ics.ICS_EXAM) |
								(with_class * cqupt_ics.ICS_CLASS)),
							enable_geo=with_geo,
							provider=provider,
							start_day=START_DAY)
		# get the first value of generator to trigger exception if would happen, which should be handled.
		# and if there is nothing thus the generator is empty, so an empty value is needed.
		try:
			first_val = await gen.__anext__()
		except Exception as e:
			raise HTTPException(status_code=503, detail=e.args[0])
		content = generate_stream_response(gen, first_val)
		return StreamingResponse(content)


def main(argv=[]):
	if DEBUG:
		logging.basicConfig(level=logging.DEBUG)
	uvicorn.run(app, host="0.0.0.0", port=PORT)


if __name__ == "__main__":
	main(sys.argv)
