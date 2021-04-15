import base64
import json
import logging
import time
import requests
from providers.basetype import ProviderBaseType

class WeCQUPTProvider(ProviderBaseType):
	APIROOT = "https://we.cqupt.edu.cn/api"
	HEADERS = {
		"Content-Type": "application/json",
		"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.2(0x18000239) NetType/WIFI Language/zh_CN",
		"Referer": "https://servicewechat.com/wx8227f55dc4490f45/89/page-frame.html",
	}

	def class_schedule(student_id: int):
		error_msg = ""
		data_raw = {"openid": None, "id": str(student_id), "timestamp": int(time.time())}
		data = {"key": base64.b64encode(json.dumps(data_raw).encode('utf-8')).decode('utf-8') }
		try: 
			r = requests.post(url = WeCQUPTProvider.APIROOT + '/get_kebiao.php', data = json.dumps(data), headers = WeCQUPTProvider.HEADERS, verify = False, timeout = 10)
			r.raise_for_status()
			response_json = r.json()
		except requests.exceptions.Timeout:
			error_msg = "课表请求超时"
			logging.debug(error_msg)
		except requests.exceptions.HTTPError as err:
			err_code = err.response.status_code
			error_msg = f"课表请求返回了 HTTP {err_code} 错误"
			logging.debug(error_msg)
		except:
			error_msg = "课表请求发生了其他网络错误"
			logging.debug(error_msg)
		else:
			try:
				if response_json["status"] != 200:
					error_msg = response_json["message"]
					return [], 0, error_msg
				classlist = []
				for day in range(0,7):
					for order in range(0,6):
						for class_obj in response_json["data"]["lessons"][day][order]:
							if len(class_obj):
								class_obj["weekday"] = day
								class_obj["begin_lesson"] = order * 2 + 1
								classlist.append(class_obj)
				course = [
						["CLASS", 
							_Class["name"], _Class["teacher"], _Class["type"], _Class["all_week"], _Class["place"], _Class["c_id"], _Class["weeks"], _Class["weekday"] + 1, 
							[_Class["begin_lesson"], _Class["begin_lesson"] + _Class["number"] - 1]
						] for _Class in classlist]
			except:
				return [], 0, "数据异常"
			return course, response_json["data"]["week"], None
		return [], 0, error_msg

	def exam_schedule(student_id: int):
		error_msg = ""
		data_raw = {"openid": None, "id": str(student_id), "timestamp": int(time.time())}
		data = {"key": base64.b64encode(json.dumps(data_raw).encode('utf-8')).decode('utf-8') }
		try: 
			r = requests.post(url = WeCQUPTProvider.APIROOT + '/get_ks.php', data = json.dumps(data), headers = WeCQUPTProvider.HEADERS, verify = False, timeout = 10)
			r.raise_for_status()
			response_json = r.json()
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
			if not response_json["data"]:
				return [], 0, None
			try:
				tests = [["TEST", _Test["course"], _Test["time"].split('-')[0], _Test["time"].split('-')[1], "未知", _Test["room"], _Test["type"],
				[int(_Test["week"])], int(_Test["day"]), _Test["number"]] for _Test in response_json["data"]]
				now_week = 0
				if len(response_json["data"]):
					sample = response_json["data"][0]
					now_week = int(int(sample["week"]) + (int(sample["days"]) / abs(int(sample["days"]))) * (abs(int(sample["days"])) // 7))
				return tests, now_week, None
			except Exception as e:
				print(e.args[0])
				return [], 0, "数据异常"
		return [], 0, error_msg
