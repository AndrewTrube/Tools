# Set of Tools for Offensive Security

## Scripts
###### bakbruter.py
Use a wordlist to bruteforce many types of backup file extensions.                               

`$ python3 ./bakbruter.py mywordlist.txt http://www.example.com/path/filename 8080`
 
###### burp-analyzer-to-csv.py
Converts exported Burp Analyzer html file to a csv file for use in a        spreadsheet.                                                                                     

`$ python3 ./burp-analyzer-to-csv.py /path/to/burp-analyzed.html [output filename]`

###### http-screenshot.py
A Python Script which takes a list of websites and uses chrome geckodriver    
to open a browser and take screenshots. Also tries to save the headers, and   
create a html page with a table containing the headers and screenshots.       

`$ python3 ./http-screenshot.py /home/user/list-of-websites.txt`

###### recon-workflow.sh
Extracts the subdomains from securitytrails.com (API KEY required) and crt.sh  
combines them with any newline seperated list of subdomains (such as from     
DNS brute force scan), checks if host is live and then feeds them to nmap.    

`$ ./recon_workflow.sh /home/user/amass-results-yahoo.txt yahoo.com`

###### ruby-cryptor.rb
Encrypts a Json object into a Ruby Session Cookie. Likewise decrypts a       
Ruby Session Cookie into a Json object. Requires knowledge of the secret key.     
`$ ruby-cryptor.rb -s '42ad55...' -e '{"id":101,"active":true}'`

###### smtp-xss-fuzz.py                                                                                                       
Python script which fuzzes for XSS vulnerabilites in SMTP apps with a web     
frontend (such as atmail).
                                                    
`$ python3 ./smtp-xss-fuzz.py -t 10.10.10.10 -u user1 -p pass1 -r admin@email.loc`

###### subdomain-takeover.sh
checks for dangling DNS CNAMEs among a list of subdomains

`$ ./subdom-tko.sh wordlist.txt target.com`


## Compiled Tools
###### TokinUtil.java
Generates a list of session tokens that can be used to bruteforce a simple   
authentication mechanism which uses the insecure java.util.Random. Seeds are 
based on timestamps in UTC.                                                                                                                          

`$ javac TokinUtil.java`  
`$ java TokinUtil 1630534604913 16305346045013 101`
