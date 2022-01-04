#!/usr/bin/env python3
# -*-coding: utf-8-*-

#################################################################################
#                     **-- HTTP Screenshot Script --**                          #
#                                                                               #
# A Python Script which takes a list of websites and uses chrome geckodriver    #
# to open a browser and take screenshots. Also tries to save the headers, and   #
# create a html page with a table containing the headers and screenshots.       #
# ex: http-screenshot.py /home/user/list-of-websites.txt                        #
#                                                                               #
# Copyright (c) 2019 Andrew Trube  <https://github.com/AndrewTrube>             #
#                                                                               #
# Permission is hereby granted, free of charge, to any person obtaining a copy  #
# of this software and associated documentation files (the "Software"), to deal #
# in the Software without restriction, including without limitation the rights  #
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell     #
# copies of the Software, and to permit persons to whom the Software is         #
# furnished to do so, subject to the following conditions:                      #
#                                                                               #
# The above copyright notice and this permission notice shall be included in all#
# copies or substantial portions of the Software.                               #
#                                                                               #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR    #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,      #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE   #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER        #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, #
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE #
# SOFTWARE.                                                                     #
#                                                                               #
#################################################################################

""" Version 0.A """
# - Add cli options
# - Format Table and headers

import time,sys,os,json,re#,argparse
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException

#init gloabl headers and regex var
headers = {}
rexegg = re.compile(r'[\r\n]{1,2}',re.MULTILINE)

def proc_logs(jsn):
  """ grab the headers from the logs 
      takes a json object from chrome 
      with log info
  """
  msg = rexegg.sub(r'',jsn)
  keys = ('message','params','headers','headersText')
  data = json.loads(msg)
  try:
    data[keys[0]][keys[1]][keys[2]][keys[3]] = data[keys[0]][keys[1]][keys[3]]
  except:
    pass
  try:
    return data[keys[0]][keys[1]][keys[2]]
  except:
    return {"null":"null"}
  
def set_options():
  """ set the browser cli options and turn on full logs """
  logging = DesiredCapabilities.CHROME
  logging['goog:loggingPrefs'] = {'performance':'ALL'}
  options = webdriver.ChromeOptions()
  options.add_argument('--no-sandbox')
  options.add_argument('--test-type')
  options.add_argument('--ignore-certificate-errors')
  options.binary_location = '/usr/bin/chromium'
  return logging,options

def screenshot(subdomains):
  """ start the webDriver and loop through the uris """
  try:
    os.mkdir(os.getcwd()+'/webhosts-screenshots')
  except:
    pass
  os.chdir(os.getcwd()+'/webhosts-screenshots')
  driver = webdriver.Chrome(options=set_options()[1],desired_capabilities=set_options()[0])
  driver.set_page_load_timeout(10)
  with open(subdomains) as fd:
    uris = fd.read().split()
  for uri in uris:
    print("Grabbing {}".format(uri))
    try:
      driver.get(("https://"+uri))
    except TimeoutException as e:
      continue
    time.sleep(1)
    logs = {}
    logs = driver.get_log('performance')
    pngname = "{}.png".format(uri)
    driver.save_screenshot(pngname)
    headers[pngname] = proc_logs([x['message'] for x in logs if re.search(r'Network.responseReceived',x['message'])][0])
    #print(headers)
    #print(resp,'\n')
    #print([x['message'] for x in logs if re.search(r'Network.responseReceived',x['message'])][0])
  driver.close()

def create_html(title):
  """ make the index html page """
  template_prefix = "<html><title>Simple-Screenshot Results for " + title + " </title><body><table style='width:100%' padding='15px' border='1px solid black'><tr><th>Headers</th><th>Screenshot</th></tr>"
  template_suffix = '</table></body></html>'
  content = []
  for x,y in headers.items():
    #print(y)
    if y == 'null':
      del headers[x]
      continue
    content.append('<tr><td> <h2>{}</h2><br><br>{} </td><td><image src="{}"></img></td></tr>'.format(re.sub(r'.png',r'',x),rexegg.sub(r'<br>',json.dumps(y,indent=4)),os.getcwd()+'/'+x))
  with open('index.html','w') as fd:
    fd.write(template_prefix)
    for z in content:
      fd.writelines(z)
    fd.write(template_suffix)

def main(t):
  screenshot(t)
  create_html(t)

if __name__ == '__main__':
  main(sys.argv[1])

