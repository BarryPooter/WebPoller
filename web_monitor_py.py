import mysql.connector
import requests
from dotenv import load_dotenv
import time
import os

load_dotenv()

# Connect to the MySQL database
conn = mysql.connector.connect(
  host=os.getenv('MYSQL_HOST'),
  user=os.getenv('MYSQL_USER'),
  password=os.getenv('MYSQL_PASS'),
  database=os.getenv('MYSQL_DB')
)

cursor = conn.cursor()

# Query the database to get the list of websites
query = "SELECT url, last_try_failed FROM websites"
cursor.execute(query)
websites = cursor.fetchall()

# Define the Discord webhook URL
discord_webhook_url = os.getenv('DISCORD_WEBHOOK_URL')

while True:
  for website in websites:
    url = website[0]
    lastTimeFailed = website[1]
  
    # Check if the website is online
    try:
      response = requests.get(url)
      status = response.status_code

      if status != 200 and lastTimeFailed == 0:
        # Send a Discord notification if the website is offline
        discord_message = f"The website {url} is offline. Response code: {status}"
        requests.post(discord_webhook_url, data={"content": discord_message})

        # Prevent another error until the website is back online.
        cursor.execute("UPDATE websites SET last_try_failed=1 WHERE url='{}'".format(url))
        conn.commit()

      if status == 200 and lastTimeFailed == 1:
        # Send a Discord notification if the website is online
        discord_message = f"The website {url} is back online! Response code: {status}"
        requests.post(discord_webhook_url, data={"content": discord_message})
        
        # Prevent another error until the website is back online.
        cursor.execute("UPDATE websites SET last_try_failed=0 WHERE url='{}'".format(url))
        conn.commit()

    except requests.exceptions.RequestException as e:
      if (lastTimeFailed == 0):
        # Send a Discord notification if the website is offline
        discord_message = f"The website {url} is offline. Error:```\n{e}\n```"
        requests.post(discord_webhook_url, data={"content": discord_message})

        # Prevent another error until the website is back online.
        cursor.execute("UPDATE websites SET last_try_failed=1 WHERE url='{}'".format(url))
        conn.commit()

  # Wait for five minutes before checking again
  time.sleep(300)