import os
import requests
import logging
import AdvancedHTMLParser
import re
from providers.basetype import ProviderBaseType

class JWZXDirectProvider(ProviderBaseType):
	APIROOT = os.getenv("JWZX_APIROOT") if os.getenv("JWZX_APIROOT") else "http://jwzx.cqupt.edu.cn/"
	HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.46"}

	def _get_weeks(mask: str):
		# mask indicates which week involves the class
		# mask sample: '11111111111111110000'
		weeks = []
		now_week = 0
		for m in mask:
			now_week += 1
			if m == '1':
				weeks.append(now_week)
		return weeks

	def _get_classes(document: AdvancedHTMLParser.AdvancedHTMLParser):
		table_tab_div: AdvancedHTMLParser.AdvancedTag = document.getElementById("kbStuTabs-table").getElementsByClassName("printTable")[0]
		form: AdvancedHTMLParser.AdvancedTag = table_tab_div.getElementsByXPath("//form")[0]
		rows = table_tab_div.getElementsByXPath("//table[1]/tr")
		now_week = 0
		
		try:
			# form contains current week
			# form.innerText sample: '\r\n\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t第9周\t\t\t\t\t\t'
			now_week = int(re.search("\\d+", re.search("第\\d+周", form.innerText).group(0)).group(0))
		except:
			now_week = 0

		class_seq = 0
		data = []

		row: AdvancedHTMLParser.AdvancedTag
		for row in rows:
			if row.children[0].innerText.strip().endswith("间歇"):
				continue
			class_seq += 1
			weekday = None
			column: AdvancedHTMLParser.AdvancedTag
			for column in row.children:
				if weekday == None:
					weekday = 0
					continue
				weekday += 1

				class_divs: AdvancedHTMLParser.AdvancedTag = column.getElementsByClassName("kbTd")

				for class_div in class_divs:
					# sample: ['马保国', '必修', '6.0学分']
					teacher, course_type, stu_point_raw = class_div.getElementsByXPath("//span[1]")[0].innerText.split(' ')
					stu_point = re.search("^(\\d+)?\\.\\d+", stu_point_raw).group(0)
					# div_texts contains course_id, class_id, location and raw_week
					# div_texts sample: [('', 0), ('A15202AXXXXXXYYYY', 1), ('AXXXYYZZ-摸鱼学导论(上)', 3), ('地点：5400 \r\n\t\t\t', 5), ('1-16周', 7)]
					div_texts = class_div.getBlocksText()
					weeks = JWZXDirectProvider._get_weeks(class_div.getAttribute("zc", ""))
					course_id = div_texts[1][0]
					class_id = div_texts[2][0].split('-')[0]
					name = div_texts[2][0].split(class_id + '-')[-1]
					location = re.sub("^地点：", "", div_texts[3][0].strip())
					raw_week = div_texts[4][0]
					# addn_element: additional information like 3节连上
					addn_element: AdvancedHTMLParser.AdvancedTag
					for addn_element in class_div.getElementsByXPath("//font[@color='#FF0000']"):
						raw_week += addn_element.innerText
					last_time = 2
					continuous_info = re.search("\\d+节连上", raw_week)
					if continuous_info:
						last_time = int(re.search("\\d+", continuous_info.group(0)).group(0))
					begin_time = class_seq * 2 - 1
					end_time = begin_time + last_time - 1
					data.append({
						"course_id": course_id,
						"class_id": class_id,
						"name": name,
						"type": course_type,
						"teacher": teacher,
						"stu_point": stu_point,
						"raw_week": raw_week,
						"weekday": weekday,
						"location": location,
						"begin_end_time": [begin_time, end_time - 1],
						"weeks": weeks
					})
		return data, now_week

	def class_schedule(student_id: int, APIROOT: str = None):
		APIROOT = APIROOT if APIROOT else JWZXDirectProvider.APIROOT
		error_msg = ""
		data = {"xh": student_id}
		document = AdvancedHTMLParser.AdvancedHTMLParser()
		try: 
			r = requests.get(url = APIROOT + '/kebiao/kb_stu.php', params = data, headers = JWZXDirectProvider.HEADERS, verify = False, timeout = 1)
			r.raise_for_status()
			document.parseStr(r.text)
		except requests.exceptions.Timeout:
			error_msg = "课表请求超时"
			logging.debug(error_msg)
		except requests.exceptions.HTTPError as err:
			err_code = err.response.status_code
			error_msg = f"课表请求返回了 HTTP {err_code} 错误"
			logging.debug(error_msg)
		except:
			error_msg = "课表请求发生了其他异常"
			logging.debug(error_msg)
		else:
			try:
				course_data, now_week = JWZXDirectProvider._get_classes(document)
				course = [
						["CLASS", 
							_Class["name"], _Class["teacher"], _Class["type"], _Class["raw_week"], _Class["location"], _Class["course_id"], _Class["weeks"], _Class["weekday"], 
							_Class["begin_end_time"]
						] for _Class in course_data]
			except:
				return [], 0, "数据异常"
			return course, now_week, None
		return [], 0, error_msg

	def _get_exams(document: AdvancedHTMLParser.AdvancedHTMLParser):
		ROW_SCHEMA = ["no", "stu_id", "stu_name", "type", "course_id", "name", "week", "weekday", "time", "location", "seat", "eligibility"]
		rows = document.getElementsByXPath("//div[@class='printTable']/table/tbody/tr")
		data = []

		for row in rows:
			# row(innerText) sample: 
			# 
			# ['2', '2020XXXXXX', '墨小菊', '半期', 'AXXXYYZZ', '摸鱼学导论(上)', '12周', '1', '第7-8节 16:10-18:10', '5400', '3', '']
			row_data = { ROW_SCHEMA[i]: row[i].innerText for i in range(1, 12) }
			time_raw = row_data["time"]
			start_time, end_time = re.search("\\d+:\\d+-\\d+:\\d+", time_raw).group(0).split('-')
			row_data.pop("time")
			row_data["start_time"] = start_time
			row_data["end_time"] = end_time
			row_data["week"] = re.search("\\d+", row_data["week"]).group(0)
			
			data.append(row_data)
			
		return data

	def exam_schedule(student_id: int, no_need_to_get_week: bool = False, APIROOT: str = None):
		APIROOT = APIROOT if APIROOT else JWZXDirectProvider.APIROOT
		error_msg = ""
		data = {"type": "stu", "id": student_id}
		document = AdvancedHTMLParser.AdvancedHTMLParser()
		now_week = 0
		if not no_need_to_get_week:
			try:
				r = requests.get(url = APIROOT + "/ksap/index.php")
				now_week = int(re.search("\\d+", re.search("第 \\d+ 周 星期", r.text).group(0)).group(0))
			except:
				now_week = 0
		try:
			r = requests.get(url = APIROOT + '/ksap/showKsap.php', params = data, headers = JWZXDirectProvider.HEADERS, verify = False, timeout = 10)
			r.raise_for_status()
			document.parseStr(r.text)
		except requests.exceptions.Timeout:
			error_msg = "考试请求超时"
			logging.debug(error_msg)
		except requests.exceptions.HTTPError as err:
			err_code = err.response.status_code
			error_msg = f"考试请求返回了 HTTP {err_code} 错误"
			logging.debug(error_msg)
		except:
			error_msg = "考试请求发生了其他网络错误"
			logging.debug(error_msg)
		else:
			try:
				exam_data = JWZXDirectProvider._get_exams(document)
				tests = [
					["TEST", 
						_Test["name"], _Test["start_time"], _Test["end_time"], _Test["eligibility"], _Test["location"], _Test["type"],
						[int(_Test["week"])], int(_Test["weekday"]), _Test["seat"]
					] for _Test in exam_data]
				return tests, now_week, None
			except:
				return [], 0, "数据异常"
		return [], 0, error_msg