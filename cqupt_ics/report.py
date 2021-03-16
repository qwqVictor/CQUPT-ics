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