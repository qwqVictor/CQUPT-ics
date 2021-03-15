import requests
from random import sample
from datetime import datetime, timedelta

# 运行前请修改参数
studentNum = 2020220202    # 你的学号
saveLoc    = "cqupt.ics"   # 文件输出目录，可填写相对路径
mode       = 1             # 模式选择: 1 仅课程，2 仅考试，3 课程+考试
reporting  = True          # 启用多次运行时课表对比功能
enableGEO  = True          # 启用教学楼定位功能（如不启用，仍可显示教室位置于标题中）

headers = {"User-Agent": "zhang shang zhong you/6.0.3 (iPhone; iOS 14.4.1; Scale/3.00)"}
requests.packages.urllib3.disable_warnings()

uid_generate = lambda: "-".join(map(lambda l: ''.join(sample("0123456789ABCDEF", l)), [8, 4, 4, 4, 12]))

def kebiao():
	data = {"stu_num": studentNum}
	try: 
		r = requests.post(url = 'https://cyxbsmobile.redrock.team/api/kebiao', data = data, headers = headers, verify = False, timeout = 10)
		r.raise_for_status()
		ansTable = r.json()
	except requests.exceptions.Timeout:
		print("课表请求超时")
	except requests.exceptions.HTTPError as err:
		errCode = err.response.status_code
		print("课表请求返回了 HTTP {errCode} 错误")
	except:
		print("课表请求发生了其他网络错误")
	else:
		kecheng = [["CLASS", _Class["course"], _Class["teacher"], _Class["type"], _Class["rawWeek"], _Class["classroom"], _Class["course_num"], 
			_Class["week"], _Class["hash_day"] + 1, [_Class["begin_lesson"], _Class["begin_lesson"] + _Class["period"] - 1]] for _Class in ansTable["data"]]
		return kecheng, ansTable["nowWeek"]
	return [], 0

def kaoshi():
	data = {"stuNum": studentNum}
	try: 
		r = requests.post(url = 'https://cyxbsmobile.redrock.team/api/examSchedule', data = data, headers = headers, verify = False, timeout = 10)
		r.raise_for_status()
		ansTable = r.json()
	except requests.exceptions.Timeout:
		print("考试请求超时")
	except requests.exceptions.HTTPError as err:
		errCode = err.response.status_code
		print("考试请求返回了 HTTP {errCode} 错误")
	except:
		print("考试请求发生了其他网络错误")
	else:
		tests = [["TEST", _Test["course"], _Test["begin_time"], _Test["end_time"], _Test["status"], _Test["classroom"], _Test["type"],
			[int(_Test["week"])], int(_Test["weekday"]), _Test["seat"]] for _Test in ansTable["data"]]
		return tests, ansTable["nowWeek"]
	return [], 0

runtime = datetime.now().strftime('%Y%m%dT%H%M%SZ')
print(f"CQUPT-ics\n学号 {studentNum}\n")

nowWeek = 0; classes = []

if mode in [1, 3]:
	temp, nowWeek = kebiao()
	classes += temp
	print(f"获得 {len(temp)} 个课程{''.join([f'【{i[1]}】' for i in temp])}\n")
if mode in [2, 3]:
	temp, nowWeek = kaoshi()
	classes += temp
	print(f"获得 {len(temp)} 个考试{''.join([f'【{i[1]}】' for i in temp])}\n")

if not len(classes):
	print("无有效课程或考试信息")
	exit()

if nowWeek != 0:
	date = datetime.now().date()
	while date.weekday() != 0:
		date -= timedelta(days = 1)
	date -= timedelta(weeks = nowWeek - 1)
	starterDay = datetime(date.year, date.month, date.day)
else:
	'''
	如您希望避免在运行中进行输入，但又频繁遇到此错误，请尝试手动设置 starterDay
	然后注释下方的代码。请注意此时输入的日期需要是校历第一周的星期一的日期
	'''
	# starterDay = datetime(2021, 3, 1) # 手动设置起始日期
	# 注释输入部分从这里开始
	print("\n未能获取当前周数，因而无法生成日历\n请手动输入本学期校历第一周内的任意一个日期")
	while True:
		print("年-月-日, 如 2021-3-1: ", end = "")
		strDate = input()
		try:
			starterDay = datetime.strptime(strDate, "%Y-%m-%d")
		except ValueError:
			print(f"  输入错误: 未能从 {strDate} 中匹配到日期")
		else:
			while starterDay.weekday() != 0:
				starterDay -= timedelta(days = 1)
			break
	# 注释输入部分从这里结束
	print(f"已更新基础日期: {starterDay.date()}\n")

classTime = [None, (8, 0), (8, 55), (10, 15), (11, 10), (14, 0), (14, 55), 
	(16, 15), (17, 10), (19, 0), (19, 55), (20, 50), (21, 45)]
weeks = [None]
for i in range(1, 30):
	singleWeek = []
	for d in range(7):
		singleWeek.append(starterDay)
		starterDay += timedelta(days = 1)
	weeks.append(singleWeek)

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

for __Class in classes:
	customGEO = ""
	CID, Name, Teacher, Kind, RawWeek, Location, classID, classWeek, classWeekday, classOrder = __Class
	print(f"处理【{f'[{classID}考试] ' if CID == 'TEST' else ''}{Name}】{'' if CID == 'TEST' else RawWeek}")

	if enableGEO:
		from dependencies import location
		customGEO = location(Location)
	else:
		customGEO = ""

	for timeWeek in classWeek:
		classDate = weeks[timeWeek][classWeekday - 1]
		if CID == "CLASS":
			startTime = classTime[classOrder[0]]
			endTime = classTime[classOrder[-1]]
			classStartTime = classDate + timedelta(minutes = startTime[0] * 60 + startTime[1])
			classEndTime = classDate + timedelta(minutes = endTime[0] * 60 + endTime[1] + 45)
			Title = f"{Name} - {Location}"
			Description = f"{classID} 任课教师: {Teacher}，该课程是{Kind}课，在{RawWeek.replace(',', '、')}行课，当前是第{timeWeek}周。"
		if CID == "TEST":
			# Name 科目，Teacher 开始时间，Kind 结束时间，RawWeek 状态，Location 地址，classID 考试类型，classOrder 座位号
			startTime = Teacher.split(":")
			endTime = Kind.split(":")
			testStatus = "正常" if RawWeek == "" else RawWeek
			classStartTime = classDate + timedelta(minutes = int(startTime[0]) * 60 + int(startTime[1]))
			classEndTime = classDate + timedelta(minutes = int(endTime[0]) * 60 + int(endTime[1]))
			Title = f"[{classID}考试] {Name} - {Location}"
			Description = f"考试在第{timeWeek}周进行，时间为{Teacher}至{Kind}，考试座位号是{classOrder}，考试状态: {testStatus}，祝考试顺利！（最终考试信息请以教务在线公布为准）"

		StartTime = classStartTime.strftime('%Y%m%dT%H%M%S')
		EndTime = classEndTime.strftime('%Y%m%dT%H%M%S')
		singleEvent = f"""
BEGIN:VEVENT
DTEND;TZID=Asia/Shanghai:{EndTime}
DESCRIPTION:{Description}
UID:{uid_generate()}
DTSTAMP:{runtime}
URL;VALUE=URI:{customGEO}
X-APPLE-TRAVEL-ADVISORY-BEHAVIOR:AUTOMATIC
SUMMARY:{Title}
CREATED:{runtime}
DTSTART;TZID=Asia/Shanghai:{StartTime}
END:VEVENT"""
		iCal += singleEvent
iCal += "\nEND:VCALENDAR"

if reporting:
	from dependencies import report
	report(classes, runtime)
print("\n正在输出 ics 文件")
with open(saveLoc, "w", encoding = "utf-8") as w:
	w.write(iCal)
print("程序结束")