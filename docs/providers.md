本程序现在已经支持多种数据源以供使用，如果您愿意，也可以自行实现数据源类，您需要实现一个类似这样的类：

```python
class CustomProvider(ProviderBaseType):
	APIROOT = "https://example.com/api"
	HEADERS = {"Some-Header": "abaaba"}

	def class_schedule(student_id: int):
		error_msg = ""
		data = {"id": student_id}
		try: 
			r = requests.post(url = CustomProvider.APIROOT + '/class', data = data, headers = CustomProvider.HEADERS, verify = False, timeout = 10)
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
				course = [
						["CLASS", 
							_Class["course"], _Class["teacher"], _Class["type"], _Class["rawWeek"], _Class["classroom"], _Class["course_num"], _Class["week"], _Class["hash_day"] + 1, 
							[_Class["begin_lesson"], _Class["begin_lesson"] + _Class["period"] - 1]
						] for _Class in response_json["data"]]
			except:
				return [], 0, "数据异常"
			return course, response_json["nowWeek"], None
		return [], 0, error_msg

	def exam_schedule(student_id: int):
		error_msg = ""
		data = {"id": student_id}
		try: 
			r = requests.post(url = CustomProvider.APIROOT + '/exam', data = data, headers = CustomProvider.HEADERS, verify = False, timeout = 10)
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
```

这两个方法均返回三个值，且都为：
- 数据结果 （是一个 `List`，各个字段意义将在下面说明）
- 当前周次
- 错误信息 （如果没有发生错误则返回 `None`）

对于课表信息，数据结果的各个字段分别为：

| Index | Type           | Sample Value      | Meaning                    |
|-------|----------------|-------------------|----------------------------|
| 0     | `str`          | `"CLASS"`         | 固定，表示为课表数据       |
| 1     | `str`          | e.g. `"托福B"`    | 课程名称                   |
| 2     | `str`          | e.g. `"可爱多"`   | 教师名称                   |
| 3     | `str`          | `"必修"`/`"选修"` | 课程类型                   |
| 4     | `str`          | e.g. `"第1-16周"` | 展示周次信息               |
| 5     | `str`          | e.g. `"5406"`     | 上课地点                   |
| 6     | `str`          | e.g. `"A114514"`  | 课程编码                   |
| 7     | `list[int]`    | e.g. `[1,2,3,4]`  | 行课周次                   |
| 8     | `int`          | e.g. `5`          | 星期 (周一开始 1-7)        |
| 9     | `list[int](2)` | e.g. `[1,2]`      | 课程起止 (如示例为第1-2节) |


对于考试信息，数据结果的各个字段分别为：

| Index | Type           | Sample Value            | Meaning                |
|-------|----------------|-------------------------|------------------------|
| 0     | `str`          | `"TEST"`                | 固定，表示为考试数据   |
| 1     | `str`          | e.g. `"计算机组成原理"` | 课程名称               |
| 2     | `str`          | e.g. `"16:10"`          | 开始时间               |
| 3     | `str`          | e.g. `"18:10"`          | 结束时间               |
| 4     | `str`          | e.g. `""`               | 考试资格有无（空为有） |
| 5     | `str`          | e.g. `"2116"`           | 考试地点               |
| 6     | `str`          | e.g. `"半期考试"`       | 类型                   |
| 7     | `list[int](1)` | e.g. `[7]`              | 考试周次               |
| 8     | `int`          | e.g. `1`                | 星期 (周一开始 1-7)    |
| 9     | `str`          | e.g. `"233"`            | 考试座号               |