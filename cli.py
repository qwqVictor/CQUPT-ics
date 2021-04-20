#!/usr/bin/env python3
import argparse
import datetime
import sys
import cqupt_ics
import providers

parser = argparse.ArgumentParser(prog="CQUPT-ICS", description="Generate ICS file schedule of CQUPT")
parser.add_argument("student_id", metavar="student_id", type=int, help="Your student ID number")
parser.add_argument("-o", "--output", type=str, help="Specify output file", default="-")
parser.add_argument("--disable-exam", help="Disable exam information in ICS file", default=False, action='store_true')
parser.add_argument("--disable-class", help="Disable class information in ICS file", default=False, action='store_true')
parser.add_argument("--disable-geo", help="Disable location data in ICS File", default=False, action='store_true')
parser.add_argument("--start-day", type=str, help="Specify the first Monday the term starts, in format YYYY-MM-dd. E.g: 1970-01-01", default="1970-01-01")
parser.add_argument("--provider", type=str, help="Specify data provider")

def main():
	config = parser.parse_args()
	writer = sys.stdout.write
	provider_list = []
	err = None
	f = None
	if config.output != "-":
		try:
			f = open(config.output)
			writer = f.write
		except:
			pass
	mode = cqupt_ics.ICS_ALL
	if config.disable_exam:
		mode ^= cqupt_ics.ICS_EXAM
	if config.disable_class:
		mode ^= cqupt_ics.ICS_CLASS
	start_day_tuple = ()
	for i in config.start_day.split('-'):
		start_day_tuple += (int(i),)

	try:
		if config.provider:
			provider_list.append(providers.providers[config.provider])
		else:
			for key in providers.providers:
				provider_list.append(providers.providers[key])
	except:
		sys.std.err.write("Invalid provider: " + config.provider)

	for provider in provider_list:
		try:
			writer(cqupt_ics.ICS_HEADER)
			for event in cqupt_ics.get_events(student_id=config.student_id, mode=mode, 
								enable_geo=(not config.disable_geo), 
								provider=provider,
								start_day=datetime.datetime(start_day_tuple[0], start_day_tuple[1], start_day_tuple[2])):
				writer(event)
			writer(cqupt_ics.ICS_FOOTER)
			err = None
			break
		except Exception as e:
			err = e

	if err:
		sys.stderr.write("Exception occured: " + str(err.args[0]))

	if f:
		f.close()
			
if __name__ == "__main__":
	main()