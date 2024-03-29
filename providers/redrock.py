import requests_html
import logging
from providers.basetype import ProviderBaseType

class RedrockProvider(ProviderBaseType):
	APIROOT = "https://be-prod.redrock.cqupt.edu.cn/magipoke-jwzx"
	HEADERS = {"User-Agent": "zhang shang zhong you/6.1.1 (iPhone; iOS 14.6; Scale/3.00)"}

	async def class_schedule(student_id: str):
		session = requests_html.AsyncHTMLSession(
			loop=requests_html.asyncio.get_event_loop(), mock_browser=False)
		error_msg = ""
		data = {"stu_num": int(student_id)}
		try: 
			r = await session.post(url = RedrockProvider.APIROOT + '/kebiao', data = data, headers = RedrockProvider.HEADERS, verify = False, timeout = 1)
			r.raise_for_status()
			response_json = r.json()
		except requests_html.requests.exceptions.Timeout:
			error_msg = "课表请求超时"
			logging.debug(error_msg)
		except requests_html.requests.exceptions.HTTPError as err:
			err_code = err.response.status_code
			error_msg = f"课表请求返回了 HTTP {err_code} 错误"
			logging.debug(error_msg)
		except Exception as e:
			error_msg = f"课表请求发生了其他网络错误: {e}"
			logging.debug(error_msg)
		else:
			try:
				course = [
						["CLASS", 
							_Class["course"], _Class["teacher"], _Class["type"], _Class["rawWeek"], _Class["classroom"], _Class["course_num"], _Class["week"], _Class["hash_day"] + 1, 
							[_Class["begin_lesson"], _Class["begin_lesson"] + _Class["period"] - 1]
						] for _Class in response_json["data"]]
			except:
				return [], 0, "数据异常"
			return course, response_json["nowWeek"], None
		return [], 0, error_msg

	async def exam_schedule(student_id: str):
		session = requests_html.AsyncHTMLSession(
			loop=requests_html.asyncio.get_event_loop(), mock_browser=False)
		error_msg = ""
		data = {"stuNum": int(student_id)}
		try: 
			r = await session.post(url = RedrockProvider.APIROOT + '/examSchedule', data = data, headers = RedrockProvider.HEADERS, verify = False, timeout = 10)
			r.raise_for_status()
			response_json = r.json()
		except requests_html.requests.exceptions.Timeout:
			error_msg = "考试请求超时"
			logging.debug(error_msg)
		except requests_html.requests.exceptions.HTTPError as err:
			err_code = err.response.status_code
			error_msg = f"考试请求返回了 HTTP {err_code} 错误"
			logging.debug(error_msg)
		except Exception as e:
			error_msg = f"考试请求发生了其他网络错误: {e}"
			logging.debug(error_msg)
		else:
			try:
				tests = [
					["TEST", 
						_Test["course"], _Test["begin_time"], _Test["end_time"], _Test["status"], _Test["classroom"], _Test["type"],
						[int(_Test["week"])], int(_Test["weekday"]), _Test["seat"]
					] for _Test in response_json["data"]]
				return tests, response_json["nowWeek"], None
			except:
				return [], 0, "数据异常"
		return [], 0, error_msg
