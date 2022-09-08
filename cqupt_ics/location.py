def get_location(loc):
	from re import search
	try:
		room = search("[0-9]{4}", loc).group()
	except AttributeError:
		room = "6666" # 不存在四位数以上的数字教室匹配
	if "YF" in loc: 
		custom_geo = """LOCATION:重庆邮电大学-逸夫科技楼\\n崇文路2号重庆邮电大学\r
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-TITLE=重庆邮电大学\r
 -逸夫科技楼\\\\n崇文路2号重庆邮电大学:geo:29.535617,106.607390"""
	elif "SL" in loc: 
		custom_geo = """LOCATION:重庆邮电大学数理学院\\n崇文路2号重庆邮电大学内\r
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-TITLE=重庆邮电大学\r
 数理学院\\\\n崇文路2号重庆邮电大学内:geo:29.530599,106.605454"""
	elif "综合实验" in loc or "实验实训室" in loc: 
		custom_geo = """LOCATION:重庆邮电大学综合实验大楼\\n南山路新力村\r
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-TITLE=重庆邮电大学\r
 综合实验大楼\\\\n南山路新力村:geo:29.524289,106.605595"""
	elif "风华" in loc or loc == "运动场1": 
		custom_geo = """LOCATION:风华运动场\\n南山街道重庆邮电大学5栋\r
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-TITLE=\r
 风华运动场\\\\n南山街道重庆邮电大学5栋:geo:29.532757,106.607510"""
	elif "太极" in loc:
		custom_geo = """LOCATION:重庆邮电大学-太极体育场\\n崇文路2号重庆邮电大学内\r
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-TITLE=重庆邮电大学\r
 -太极体育场\\\\n崇文路2号重庆邮电大学内:geo:29.532940,106.609072"""
	elif "乒乓球" in loc:
		custom_geo = """LOCATION:风雨操场(乒乓球馆)\\n崇文路2号重庆邮电大学内\r
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-TITLE=风雨操场(乒乓球馆)\\\\n\r
 崇文路2号重庆邮电大学内:geo:29.534230,106.608516"""
	elif "篮球" in loc or "排球" in loc:
		custom_geo = """LOCATION:重庆邮电学院篮球排球馆\\n崇文路2号重庆邮电大学内\r
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-TITLE=重庆邮电学院篮球排球馆\\\\n\r
 崇文路2号重庆邮电大学内:geo:29.534025,106.609148"""
	elif room[0] == "1":
		custom_geo = """LOCATION:重庆邮电大学-光电工程学院\\n崇文路2号重庆邮电大学内\r
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-TITLE=重庆邮电大学\r
 -光电工程学院\\\\n崇文路2号重庆邮电大学内:geo:29.531478,106.605921"""
	elif room[0] == "2": 
		custom_geo = """LOCATION:重庆邮电大学二教学楼\\n崇文路2号重庆邮电大学内\r
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-TITLE=重庆邮电大学\r
 二教学楼\\\\n崇文路2号重庆邮电大学内:geo:29.532703,106.606747"""
	elif room[0] == "3": 
		custom_geo = """LOCATION:重庆邮电大学第三教学楼\\n崇文路2号\r
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-TITLE=重庆邮电大学\r
 第三教学楼\\\\n崇文路2号:geo:29.535119,106.609114"""
	elif room[0] == "4": 
		custom_geo = """LOCATION:重庆邮电大学第四教学楼\\n崇文路2号\r
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-TITLE=重庆邮电大学\r
 第四教学楼\\\\n崇文路2号:geo:29.536107,106.608759"""
	elif room[0] == "5": 
		custom_geo = """LOCATION:重庆邮电大学-国际学院\\n崇文路2号重庆邮电大学内\r
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-TITLE=重庆邮电大学\r
 -国际学院\\\\n崇文路2号重庆邮电大学内:geo:29.536131,106.610090"""
	elif room[0] == "8": 
		custom_geo = """LOCATION:重庆邮电大学八教学楼A栋\\n崇文路2号重庆邮电大学内\r
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-TITLE=重庆邮电大学\r
 八教学楼A栋\\\\n崇文路2号重庆邮电大学内:geo:29.535322,106.611020"""
	else: #Fallback
		custom_geo = """LOCATION:重庆邮电大学\\n崇文路2号\r
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-TITLE=\r
 重庆邮电大学\\\\n崇文路2号:geo:29.530807,106.607617"""
	custom_geo = f'\r\n{custom_geo}\r\nGEO:{custom_geo.split("geo:")[1].replace(",", ";")}'
	return custom_geo