#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Import libraries
import requests, datetime, time, os, schedule, pandas as pd
from bs4 import BeautifulSoup
import smtplib, ssl


#I show how to use the scheduler and send automated emails using SMTP with Gmail
def track_prices():
    url = 'https://www.bose.com/en_us/products/headphones/over_ear_headphones/quietcomfort-35-wireless-ii.html#v=qc35_ii_silver'
    html_text = requests.get(url).text
    soup=BeautifulSoup(html_text,'html.parser')
    
    price = soup.find('div',{'class':'bose-price__price bose-price__price--productPage'}).text
    
    
    #Removes the dollar sign
    price = price[1:]
    
    #Get current time stamp
        #The strftime part formats the date so that it removes the time measured less than 1 second. easier to read
    time_retrieved = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    test_string = time_retrieved + ", " + price
    
    file_name = r'name of file where the prices will be stored'
    
    with open(file_name,"a") as f:
        f.write(test_string + '\n')
        f.close()
    
    #Check if there is only one price in the file
    if sum(1 for line in open(file_name)) == 1:
        pass
    else:  
        price_list = open(file_name,"r").read().split()
        price_difference = round(float(price_list[-1]) - float(price_list[-4]),2) #have to do float(price) to perform calculation
        
        if price_difference != 0:
            #Email Portion
            
            if price_difference > 0: #Price has increased
                email_message_info = ['increased']
            elif price_difference < 0: #price has decreased
                email_message_info = ['decreased']
                
            email_message_info.append(abs(price_difference))
            
            email = open(r'your email').read()
            password=open(r'your password').read()
            
            port = 465  # For SSL
            smtp_server = "smtp.gmail.com"
            sender_email = email  # Enter your address
            receiver_email = email  # Enter receiver address
            
            
            subject = "Price has {}".format(email_message_info[0])
            
            email_body = "The price has {} by {} The new price is {}. Go check it out here: {}""".format(email_message_info[0],
                                                                                                         email_message_info[1],
                                                                                                         float(price),
                                                                                                         url)
            
            message = 'Subject: {}\n\n{}'.format(subject,email_body)
    
    
            # Create a secure SSL context
            context = ssl.create_default_context()
            
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(email, password)
                server.sendmail(sender_email, receiver_email, message)


# For test purposes, do it every 5 seconds
schedule.every(5).hours.do(track_prices)

while True:
    schedule.run_pending()
    time.sleep(1)
