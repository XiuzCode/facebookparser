# coded by: salism3
# 23 - 05 - 2020 23:18 (Malam Takbir)

from .checker import check_login
from .output import Output, People, Group
from . import parsing
import re

@check_login
def msgUrl(ses, next = None):
	html = ses.session.get("https://mbasic.facebook.com/messages" if not next else next).text
	data = parsing.parsing_href(html, "/read/")
	next = parsing.parsing_href_regex(html, r"[?]pageNum.*selectable", one = True)
	return Output(ses, msgUrl, items = data, next = next, html = html)

@check_login
def myGroup(ses):
  html = ses.session.get("https://mbasic.facebook.com/groups/?seemore&refid=27").text
  data = parsing.parsing_href_regex(html, r"/groups/\d+\W", bs4_class = True)
  data = [(x.text, re.search(r"/(\d+)\W", x["href"]).group(1)) for x in data]
  return Output(ses, myGroup, items = data, html = html)

def find_people(ses, name):
  html = ses.session.get("https://mbasic.facebook.com/search/people/?q={}&source=filter&isTrending=0".format(name)).text
  url = parsing.parsing_href(html, "__xts__", one = True)
  try:
    html = ses.session.get(url).text
    return People(ses, html)
  except:
    return
 
def find_group(ses, name):
  html = ses.session.get("https://mbasic.facebook.com/search/groups/?q={}&source=filter&isTrending=0".format(name)).text
  url = parsing.parsing_href(html, "__xts__", one = True)
  try:
    # print("in try")
    id_ = re.search(r"/(\d+)\Wrefid", url).group(1)
    html = ses.session.get("https://mbasic.facebook.com/groups/{}?view=info".format(id_)).text
    return Group(ses, html)
  except:
    return
