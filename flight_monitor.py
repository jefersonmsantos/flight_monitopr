from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os
from dotenv import load_dotenv
from pathlib import Path 


i =1
while i ==1:
    driver=webdriver.Chrome()

    driver.get('https://www.kayak.com.br/flights/GRU-FRA/2020-12-15/2021-01-05?sort=price_a&fs=stops=-2')


    time.sleep(20)
    content=driver.page_source
    soup=BeautifulSoup(content)

    for span in soup.findAll('span',attrs={'class':'js-label js-price _itL _ibU _ibV _idj _kKW'}):
        price=span.text[-4:]
        
    if int(price)<=3500:

        # create message object instance
        msg = MIMEMultipart()
        
        
        message = "Encontramos um voo por "+price

        env_path = Path('.')/'.env'
        load_dotenv(dotenv_path = env_path)
        
        # setup the parameters of the message
        password = os.getenv('PASSWORD')
        msg['From'] = os.getenv('FROM')
        msg['To'] = os.getenv('TO')
        msg['Subject'] = "Encontramos um voo"
        

        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        
        #create server
        server = smtplib.SMTP('smtp.gmail.com: 587')
        
        server.starttls()
        
        # Login Credentials for sending the mail
        server.login(msg['From'], password)
        
        
        # send the message via the server.
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        
        server.quit()

    driver.quit()
    time.sleep(7200)