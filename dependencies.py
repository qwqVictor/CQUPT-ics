def location(Location):
	from re import search
	try:
		room = search("[0-9]{4}", Location).group()
	except AttributeError:
		room = "6666" # 不存在四位数以上的数字教室匹配
	if "YF" in Location: 
		customGEO = """LOCATION:重庆邮电大学-逸夫科技楼\\n崇文路2号重庆邮电大学
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-APPLE-MAPKIT-HANDLE=;X-APPLE-RADIUS=200;X-TITLE=重庆邮电大学
 -逸夫科技楼\\\\n崇文路2号重庆邮电大学:geo:29.535617,106.607390"""
	elif "SL" in Location: 
		customGEO = """LOCATION:重庆邮电大学数理学院\\n崇文路2号重庆邮电大学内
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-APPLE-MAPKIT-HANDLE=;X-APPLE-RADIUS=200;X-TITLE=重庆邮电大学
 数理学院\\\\n崇文路2号重庆邮电大学内:geo:29.530599,106.605454"""
	elif "综合实验楼" in Location: 
		customGEO = """LOCATION:重庆邮电大学综合实验大楼\\n南山路新力村
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-APPLE-MAPKIT-HANDLE=;X-APPLE-RADIUS=200;X-TITLE=重庆邮电大学
 综合实验大楼\\\\n南山路新力村:geo:29.524289,106.605595"""
	elif "风华" in Location or Location == "运动场1": 
		customGEO = """LOCATION:风华运动场\\n南山街道重庆邮电大学5栋
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-APPLE-MAPKIT-HANDLE=;X-APPLE-RADIUS=200;X-TITLE=
 风华运动场\\\\n南山街道重庆邮电大学5栋:geo:29.532757,106.607510"""
	elif "太极" in Location:
		customGEO = """LOCATION:重庆邮电大学-太极体育场\\n崇文路2号重庆邮电大学内
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-APPLE-MAPKIT-HANDLE=;X-APPLE-RADIUS=200;X-TITLE=重庆邮电大学
 -太极体育场\\\\n崇文路2号重庆邮电大学内:geo:29.532940,106.609072"""
	elif "乒乓球" in Location:
		customGEO = """LOCATION:风雨操场(乒乓球馆)\\n崇文路2号重庆邮电大学内
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-APPLE-MAPKIT-HANDLE=;X-APPLE-RADIUS=200;X-TITLE=风雨操场(乒乓球馆)\\\\n
 崇文路2号重庆邮电大学内:geo:29.534230,106.608516"""
	elif "篮球" in Location or "排球" in Location:
		customGEO = """LOCATION:重庆邮电学院篮球排球馆\\n崇文路2号重庆邮电大学内
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-APPLE-MAPKIT-HANDLE=;X-APPLE-RADIUS=200;X-TITLE=重庆邮电学院篮球排球馆\\\\n
 崇文路2号重庆邮电大学内:geo:29.534025,106.609148"""
	elif room[0] == "1":
		customGEO = """LOCATION:重庆邮电大学-光电工程学院\\n崇文路2号重庆邮电大学内
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-APPLE-MAPKIT-HANDLE=;X-APPLE-RADIUS=200;X-TITLE=重庆邮电大学
 -光电工程学院\\\\n崇文路2号重庆邮电大学内:geo:29.531478,106.605921"""
	elif room[0] == "2": 
		customGEO = """LOCATION:重庆邮电大学二教学楼\\n崇文路2号重庆邮电大学内
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-APPLE-MAPKIT-HANDLE=;X-APPLE-RADIUS=200;X-TITLE=重庆邮电大学
 二教学楼\\\\n崇文路2号重庆邮电大学内:geo:29.532703,106.606747"""
	elif room[0] == "3": 
		customGEO = """LOCATION:重庆邮电大学第三教学楼\\n崇文路2号
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-APPLE-MAPKIT-HANDLE=;X-APPLE-RADIUS=200;X-TITLE=重庆邮电大学
 第三教学楼\\\\n崇文路2号:geo:29.535119,106.609114"""
	elif room[0] == "4": 
		customGEO = """LOCATION:重庆邮电大学第四教学楼\\n崇文路2号
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-APPLE-MAPKIT-HANDLE=;X-APPLE-RADIUS=200;X-TITLE=重庆邮电大学
 第四教学楼\\\\n崇文路2号:geo:29.536107,106.608759"""
	elif room[0] == "5": 
		customGEO = """LOCATION:重庆邮电大学-国际学院\\n崇文路2号重庆邮电大学内
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-APPLE-MAPKIT-HANDLE=;X-APPLE-RADIUS=200;X-TITLE=重庆邮电大学
 -国际学院\\\\n崇文路2号重庆邮电大学内:geo:29.536131,106.610090"""
	elif room[0] == "8": 
		customGEO = """LOCATION:重庆邮电大学八教学楼A栋\\n崇文路2号重庆邮电大学内
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-APPLE-MAPKIT-HANDLE=;X-APPLE-RADIUS=200;X-TITLE=重庆邮电大学
 八教学楼A栋\\\\n崇文路2号重庆邮电大学内:geo:29.535322,106.611020"""
	else: #Fallback
		customGEO = """LOCATION:重庆邮电大学\\n崇文路2号
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-APPLE-MAPKIT-HANDLE=;X-APPLE-RADIUS=200;X-TITLE=
 重庆邮电大学\\\\n崇文路2号:geo:29.530807,106.607617"""
	return "\n"+ customGEO

def report(classes, runtime):
	import difflib
	flag = False
	write = "\n".join([f"{i}" for i in classes])
	try:
		with open("classes.txt", encoding = "utf-8") as r:
			org = r.read()
	except FileNotFoundError:
		print("\n首次运行，将为下次运行写入 classes.txt")
		flag = True
	with open("classes.txt", "w", encoding = "utf-8") as w:
		w.write(write)
	if flag:
		return
	if org != write:
		print("\n监测到课表变化，正在生成 DIFF")
		diff = difflib.unified_diff(org.split("\n"), write.split("\n"))
		fileDiff = f"""
<!DOCTYPE html>

<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CQUPT-ics</title>
</head>

<body><pre><code>
CQUPT-ics
生成于 {runtime}\n
"""
		fileDiff += "\n".join(diff) + "\n</code></pre></body></html>"
		with open("classdiff.html", "w", encoding = "utf-8") as w:
			w.write(fileDiff)
		print("已生成 classdiff.html")
	else:
		print("\n未监测到课表变化")