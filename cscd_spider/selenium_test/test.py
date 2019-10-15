import re

year = "2010(10)"
comp = re.compile('[(\d){4}($]')
print(comp.search(year).span())
