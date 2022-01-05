from bs4 import BeautifulSoup
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import base64

def sendoveremail(link):
    mail_content = '''Hello,
    Here is today's The Hindu Newspaper!!
    
    Link to the newspaper: %s''' % link
    #The mail addresses and password

    # uncomment these lines with appropriate values
    # sender_address = base64.b64decode(BASE 64 ENCODED SENDER EMAIL ADDRESS).decode('utf-8')
    # sender_pass = base64.b64decode(BASE 64 ENCODED SENDER EMAIL PASSWORD).decode('utf-8')
    # receiver_address = base64.b64decode(BASE 64 ENCODED RECIEVER EMAIL ADDRESS).decode('utf-8')
    
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'The Hindu Epaper | %s' % datetime.datetime.today().strftime('%Y-%m-%d')   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()

def get_newspaper(download=False, sendmail=True):
    url = "https://dailyepaper.in/the-hindu-pdf-free-download-04-jan-2022/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    div = soup.find_all("div", attrs={"class": "entry-content mh-clearfix"})[0]
    anchors = div.find_all("a")

    for i in anchors:
        if "vk.com" in i["href"]:
            break

    pdf = i["href"]
    resp = requests.get(pdf)
    next_soup = BeautifulSoup(resp.text, 'html.parser')

    iframe = next_soup.find_all("iframe")[0]
    newspaper = iframe["src"]

    print("Got the newspaper... ;)")

    if sendmail:
        print("Sending link over email...")
        sendoveremail(newspaper)

    if download:
        print("Downloading the newspaper...")
        nwp_response = requests.get(newspaper)
        with open(r"C:\\Users\\himanshu_sharma15\\Downloads\\today.pdf", 'wb') as f:
            f.write(nwp_response.content)

get_newspaper(download=True, sendmail=True)