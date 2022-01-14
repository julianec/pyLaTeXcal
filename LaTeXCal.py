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

class MonthlyOverview:
	def __init__(self, month, year):
		self.month_no = month
		self.year = year
		# create a new calendar object called my_calendar
		self.my_calendar = cal.Calendar()
		self.month_name = cal.month_name[self.month_no] # January is at index 1! 0 = empty string

	# method to return a string for blank days at the start of the month
	# add up to six '\BlankDay' to blankdays to pass to jinja
	def getBlankDayString(self):
		# create an iterator for the days of a given year and month as numbers 
		# where days not belonging to the given month are 0.
		month = self.my_calendar.itermonthdays(self.year, self.month_no)
		blankdays = ''
		for day in month:
			if day == 0:
				blankdays = blankdays +'\BlankDay' + '\n'
			else:
				# we don't want '\BlankDay's for the days of the week after the end of the month
				break
		return blankdays
		 
	# method to return a string for the days of the month
	def getDayString(self): 
		# create an iterator for the days of a given year and month as numbers 
		# where days not belonging to the given month are 0.
		month = self.my_calendar.itermonthdays(self.year, self.month_no)
		days = ''
		for day in month:
			if day != 0:
				days = days +'\day{}{\\vspace{2.0cm}} % day '+ str(day) + '\n'
		return days

# create a monthly overview for January 2022
myCal = MonthlyOverview(1, 2022)

template = latex_jinja_env.get_template('calendar.tex.jinja2')
print(template.render(month=myCal.month_name, year=myCal.year, blankdays=myCal.getBlankDayString(), days=myCal.getDayString()))
