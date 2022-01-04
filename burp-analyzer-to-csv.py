#!/usr/bin/env python3

#################################################################################
#                 **-- Convert Burp Analyzer to CSV --**                        #
# Converts exported Burp Analyzer html file to a csv file for use in a          #
# spreadsheet.                                                                  #                   
# ex: burp-analyzer-to-csv.py /path/to/burp-analyzed.html [output filename]     #  
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
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR    #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,      #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE   #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER        #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, #
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE #
# SOFTWARE.                                                                     #
#                                                                               #
#################################################################################

import sys,csv,bs4

def parse_me(html):
  parsed = bs4.BeautifulSoup(html, features='lxml')
  soup = parsed.find('h2',string='Dynamic URLs').next_sibling
  params = [x.contents for x in soup.findChildren('ul', recursive=True)]
  return {x:y for x,y in zip([x.text for x in soup.findChildren('li', recursive=False)],[[y.text for y in params[x]] for x in range(0,len(params))])}
  
def to_csv(parsed_html):
  if len(sys.argv) < 3:
    fname = 'burp-analyzed'
  else:
    fname = sys.argv[2]
  with open('{}.csv'.format(fname),'w',newline='') as csvfd:
    writer = csv.DictWriter(csvfd,fieldnames=parsed_html.keys())
    writer.writeheader()
    writer.writerow(parsed_html)    

if __name__ == '__main__':
  try: 
    burp_html = sys.argv[1]
  except:
    print('Usage:python3 burp-analyzer-to-csv.py [/path/to/exported_burp_analyzer_file] [output_file_name (defualt: burp-analyzed)]')
    exit(1)
  with open(burp_html) as fd:
    to_csv(parse_me(fd))


