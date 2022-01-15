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
import click # we want to build a command line interface

class MonthlyOverview:
	""" Class for creating LaTeX output for the calendar template. Expects Month [1-12] and year [YYYY] """
	def __init__(self, month, year):
		self.month_no = month
		self.year = year
		# create a new calendar object called my_calendar
		self.my_calendar = cal.Calendar()
		self.month_name = cal.month_name[self.month_no] # January is at index 1! 0 = empty string

	def getBlankDayString(self):
		""" Method to return a "LaTeX string for blank days at the start of the month.
		Add up to six '\BlankDay' to blankdays to pass to jinja """
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
		 
	def getDayString(self): 
		""" Method to return a LaTeX string for the days of the month. """
		# create an iterator for the days of a given year and month as numbers 
		# where days not belonging to the given month are 0.
		month = self.my_calendar.itermonthdays(self.year, self.month_no)
		days = ''
		for day in month:
			if day != 0:
				days = days +'\day{}{\\vspace{2.0cm}} % day '+ str(day) + '\n'
		return days

""" 
Chain of decorations that all affect def cli in the end. 
click.intRange() does range validation so the month is always between 1 and 12 and the year is always an integer starting from year 0 as the calendar package allows.
"""
@click.command()
@click.option(
	"--year", default=2022, type=click.IntRange(0), help="Specify the year in YYYY."
)
@click.option(
	"--month", default=1, type=click.IntRange(1, 12), help="Specify the Month as a value from 1 - 12."
)
@click.option(
	"output", default="-", type=click.File("w")
)
def cli(year, month):
	# create a monthly overview for Month in year 
	myCal = MonthlyOverview(month, year)
	# open the template file
	template = latex_jinja_env.get_template('calendar.tex.jinja2')
	# create the LaTeX output from template and myCal
	output.write(template.render(month=myCal.month_name, year=myCal.year, blankdays=myCal.getBlankDayString(), days=myCal.getDayString()))
	output.flush()

# execute function if called directly via python3 and not imported. 
if __name__ == "__main__":
	cli()
