#!/usr/bin/env ruby

#################################################################################
#                  *-- Ruby Cookie Encryptor/Decryptor --*                      #
#                                                                               #
#  Encrypts a Json object into a Ruby Session Cookie. Likewise decrypts a       #
#  Ruby Session Cookie into a Json object. Requires knowledge of the secret key #    
#  ex: ruby-cryptor.rb -s '42ad55...' -e '{"id":101,"active":true}'             #
#                                                                               #
# Copyright (c) 2020 Andrew Trube  <https://github.com/AndrewTrube>             #
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
##################################################################################

require 'cgi'
require 'json'
require 'active_support'
require 'optparse'

def crypt_session_cookie(cookie, secret_key_base, switch)
  salt = "encrypted cookie"
  signed_salt = "signed encrypted cookie"
  key_generator = ActiveSupport::KeyGenerator.new(secret_key_base, iterations: 1000)
  
  if switch == true 
    cookie = CGI::unescape(cookie)
    secret = key_generator.generate_key(salt)[0, 32]
    sign_secret = key_generator.generate_key(signed_salt)
    encryptor = ActiveSupport::MessageEncryptor.new(secret, sign_secret, serializer: JSON)
    encryptor.decrypt_and_verify(cookie)
  else
    secret = key_generator.generate_key(salt)[0, 32]
    sign_secret = key_generator.generate_key(signed_salt)
    crypt = ActiveSupport::MessageEncryptor.new(secret, sign_secret, serializer: JSON)
    crypt.encrypt_and_sign(cookie)
  end
end
    
    
if __FILE__ == $0
  options = {}
  OptionParser.new do |parser|
    parser.banner = "Usage: ruby-cryptor.rb --secret=SECRET_KEY -d [ENCRYPTED COOKIE] OR -e [JSON SESS TOKEN TO ENCRYPT]"
        
    parser.on('-sKEY','--secret=KEY',String,'Ruby secret key') do |key|
      options[:secret] = key
    end  
    
    parser.on('-d[COOKIE]','--cookie[=COOKIE]',String, "Ruby cookie to decrypt") do |cookie|
      puts options[:secret]
      puts "#{crypt_session_cookie(cookie,options[:secret],true)}"
    end

    parser.on('-e[JSON_OBJECT]','--json[=JSON_OBJECT]',String,"Json session object to encrypt") do |jsn|
      puts "#{crypt_session_cookie(jsn,options[:secret],nil)}"
    end
  
  end.parse!

end
