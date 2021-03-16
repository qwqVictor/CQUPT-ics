import requests
import logging
from cqupt_ics.location import get_location
from cqupt_ics.report import report
from random import sample
from datetime import datetime, timedelta

ICS_CLASS = 1
ICS_EXAM = 2
ICS_ALL = ICS_CLASS | ICS_EXAM

APIROOT = "https://cyxbsmobile.redrock.team/api"
HEADERS = {"User-Agent": "zhang shang zhong you/6.0.3 (iPhone; iOS 14.4.1; Scale/3.00)"}

requests.packages.urllib3.disable_warnings()

uid_generate = lambda: "-".join(map(lambda l: ''.join(sample("0123456789ABCDEF", l)), [8, 4, 4, 4, 12]))

def class_schedule(student_id: int):
	data = {"stu_num": student_id}
	try: 
		r = requests.post(url = APIROOT + '/kebiao', data = data, headers = HEADERS, verify = False, timeout = 10)
		r.raise_for_status()
		response_json = r.json()
	except requests.exceptions.Timeout:
		logging.debug("课表请求超时")
	except requests.exceptions.HTTPError as err:
		err_code = err.response.status_code
		logging.debug(f"课表请求返回了 HTTP {err_code} 错误")
	except:
		logging.debug("课表请求发生了其他网络错误")
	else:
		try:
			course = [["CLASS", _Class["course"], _Class["teacher"], _Class["type"], _Class["rawWeek"], _Class["classroom"], _Class["course_num"], 
				_Class["week"], _Class["hash_day"] + 1, [_Class["begin_lesson"], _Class["begin_lesson"] + _Class["period"] - 1]] for _Class in response_json["data"]]
		except:
			return [], 0
		return course, response_json["nowWeek"]
	return [], 0

def exam_schedule(student_id: int):
	data = {"stuNum": student_id}
	try: 
		r = requests.post(url = APIROOT + '/examSchedule', data = data, headers = HEADERS, verify = False, timeout = 10)
		r.raise_for_status()
		response_json = r.json()
	except requests.exceptions.Timeout:
		logging.debug("考试请求超时")
	except requests.exceptions.HTTPError as err:
		err_code = err.response.status_code
		logging.debug(f"考试请求返回了 HTTP {err_code} 错误")
	except:
		logging.debug("考试请求发生了其他网络错误")
	else:
		tests = [["TEST", _Test["course"], _Test["begin_time"], _Test["end_time"], _Test["status"], _Test["classroom"], _Test["type"],
			[int(_Test["week"])], int(_Test["weekday"]), _Test["seat"]] for _Test in response_json["data"]]
		return tests, response_json["nowWeek"]
	return [], 0

def get_ics(student_id: int, mode: int, enable_geo: bool = True, start_day: datetime = datetime(1970, 1, 1)):
	runtime = datetime.now().strftime('%Y%m%dT%H%M%SZ')
	now_week = 0
	classes = []
	if mode & ICS_CLASS:
		temp, temp2 = class_schedule(student_id)
		now_week = max(now_week, temp2)
		classes += temp
		logging.debug(f"获得 {len(temp)} 个课程{''.join([f'【{i[1]}】' for i in temp])}\n")
	if mode & ICS_EXAM:
		temp, temp2 = exam_schedule(student_id)
		now_week = max(now_week, temp2)
		classes += temp
		logging.debug(f"获得 {len(temp)} 个考试{''.join([f'【{i[1]}】' for i in temp])}\n")

	if not len(classes):
		return ''

	if now_week != 0:
		date = datetime.now().date()
		while date.weekday() != 0:
			date -= timedelta(days = 1)
		date -= timedelta(weeks = now_week - 1)
		start_day = datetime(date.year, date.month, date.day)

	class_time = [None, (8, 0), (8, 55), (10, 15), (11, 10), (14, 0), (14, 55), 
		(16, 15), (17, 10), (19, 0), (19, 55), (20, 50), (21, 45)]
	weeks = [None]
	for i in range(1, 30):
		single_week = []
		for d in range(7):
			single_week.append(start_day)
			start_day += timedelta(days = 1)
		weeks.append(single_week)

	iCal = """BEGIN:VCALENDAR
METHOD:PUBLISH
VERSION:2.0
X-WR-CALNAME:课表
PRODID:-//Apple Inc.//macOS 11.2.3//EN
X-APPLE-CALENDAR-COLOR:#711A76
X-WR-TIMEZONE:Asia/Shanghai
CALSCALE:GREGORIAN
BEGIN:VTIMEZONE
TZID:Asia/Shanghai
BEGIN:STANDARD
TZOFFSETFROM:+0900
RRULE:FREQ=YEARLY;UNTIL=19910914T170000Z;BYMONTH=9;BYDAY=3SU
DTSTART:19890917T020000
TZNAME:GMT+8
TZOFFSETTO:+0800
END:STANDARD
BEGIN:DAYLIGHT
TZOFFSETFROM:+0800
DTSTART:19910414T020000
TZNAME:GMT+8
TZOFFSETTO:+0900
RDATE:19910414T020000
END:DAYLIGHT
END:VTIMEZONE"""

	for _class in classes:
		custom_geo = ""
		cid, name, teacher, kind, raw_week, location, class_id, class_week, class_weekday, class_order = _class
		logging.debug(f"处理【{f'[{class_id}考试] ' if cid == 'TEST' else ''}{name}】{'' if cid == 'TEST' else raw_week}")

		if enable_geo:
			custom_geo = get_location(location)
		else:
			custom_geo = ""

		for time_week in class_week:
			class_date = weeks[time_week][class_weekday - 1]
			if cid == "CLASS":
				start_time = class_time[class_order[0]]
				end_time = class_time[class_order[-1]]
				class_start_time = class_date + timedelta(minutes = start_time[0] * 60 + start_time[1])
				class_end_time = class_date + timedelta(minutes = end_time[0] * 60 + end_time[1] + 45)
				title = f"{name} - {location}"
				description = f"{class_id} 任课教师: {teacher}，该课程是{kind}课，在{raw_week.replace(',', '、')}行课，当前是第{time_week}周。"
			if cid == "TEST":
				# Name 科目，Teacher 开始时间，Kind 结束时间，RawWeek 状态，Location 地址，classID 考试类型，classOrder 座位号
				start_time = teacher.split(":")
				end_time = kind.split(":")
				test_status = "正常" if raw_week == "" else raw_week
				class_start_time = class_date + timedelta(minutes = int(start_time[0]) * 60 + int(start_time[1]))
				class_end_time = class_date + timedelta(minutes = int(end_time[0]) * 60 + int(end_time[1]))
				title = f"[{class_id}考试] {name} - {location}"
				description = f"考试在第{time_week}周进行，时间为{teacher}至{kind}，考试座位号是{class_order}，考试状态: {test_status}，祝考试顺利！（最终考试信息请以教务在线公布为准）"

			start_time = class_start_time.strftime('%Y%m%dT%H%M%S')
			end_time = class_end_time.strftime('%Y%m%dT%H%M%S')
			single_event = f"""
BEGIN:VEVENT
DTEND;TZID=Asia/Shanghai:{end_time}
DESCRIPTION:{description}
UID:{uid_generate()}
DTSTAMP:{runtime}
URL;VALUE=URI:{custom_geo}
X-APPLE-TRAVEL-ADVISORY-BEHAVIOR:AUTOMATIC
SUMMARY:{title}
CREATED:{runtime}
DTSTART;TZID=Asia/Shanghai:{start_time}
END:VEVENT"""
			iCal += single_event
	iCal += "\nEND:VCALENDAR"
	return iCal

	# if reporting:
		# report(classes, runtime)
