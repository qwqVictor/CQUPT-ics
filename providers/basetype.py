class ProviderBaseType:
	APIROOT = ""
	HEADERS = {}

	async def class_schedule(student_id: str):
		return [], 0, ""

	async def exam_schedule(student_id: str):
		return [], 0, ""