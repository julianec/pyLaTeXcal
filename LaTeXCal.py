import jinja2
import os
from jinja2 import Template
import calendar as cal
latex_jinja_env = jinja2.Environment(
	block_start_string = '\BLOCK{',
	block_end_string = '}',
	variable_start_string = '\VAR{',
	variable_end_string = '}',
	comment_start_string = '\#{',
	comment_end_string = '}',
	line_statement_prefix = '%%',
	line_comment_prefix = '%#',
	trim_blocks = True,
	autoescape = False,
	loader = jinja2.FileSystemLoader(os.path.abspath('.'))
)
# create a new calendar object called my_calendar
my_calendar = cal.Calendar()
month_no = 1 # January
month_name = cal.month_name[month_no] # January is at index 1! 0 = empty string
year = 2022 # 2022

# create string for blank days at the start of the month
# add up to six '\BlankDay' to blankdays to pass to jinja
def createBlankDayString(blankyear, blankmonth_no):
	# create an iterator for the days of a given year and month as numbers 
	# where days not belonging to the given month are 0.
	month = my_calendar.itermonthdays(blankyear, blankmonth_no)
	blankdays = ''
	for day in month:
		if day == 0:
			blankdays = blankdays +'\BlankDay' + '\n'
		else:
			# we don't want '\BlankDay's for the days of the week after the end of the month
			break
	return blankdays
		 
# create string for the days of the month
def createDayString(daystringyear, daystringmonth_no): 
	# create an iterator for the days of a given year and month as numbers 
	# where days not belonging to the given month are 0.
	month = my_calendar.itermonthdays(daystringyear, daystringmonth_no)
	days = ''
	for day in month:
		if day != 0:
			#days = days +'\day{}{\\vspace{2.5cm}} % day '+ str(day) + '\n'
			days = days +'\day{}{\\vspace{2.0cm}} % day '+ str(day) + '\n'
	return days

blankdays = createBlankDayString(year, month_no)
days = createDayString(year, month_no)

template = latex_jinja_env.get_template('calendar.tex.jinja2')
print(template.render(month=month_name, year=year, blankdays=blankdays, days=days))
