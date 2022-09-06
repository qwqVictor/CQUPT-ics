class ProviderBaseType:
	APIROOT = ""
	HEADERS = {}

	async def class_schedule(student_id: int):
		return [], 0, ""

	async def exam_schedule(student_id: int):
		return [], 0, ""