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

requestHeaders = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/json,application/xml;q=0.9,*/*;q=0.8',
    'Connection': 'close'
}

pollSpeed = int(os.getenv('POLL_FREQUENCY_SEC'))


# Query the database to get the list of websites
# Define the Discord webhook URL
discord_webhook_url = os.getenv('DISCORD_WEBHOOK_URL')

while True:
  # Get latest information from MySQL database.
  cursor = conn.cursor()
  cursor.execute("SELECT url, last_try_failed FROM websites")
  websites = cursor.fetchall()
  conn.commit()

  for website in websites:
    url = website[0]
    lastTimeFailed = website[1]

    # Check if the website is online
    try:
      response = requests.get(url, headers=requestHeaders)
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
      if lastTimeFailed == 0:
        # Send a Discord notification if the website is offline
        discord_message = f"The website {url} is offline. Error:```\n{e}\n```"
        requests.post(discord_webhook_url, data={"content": discord_message})

        # Prevent another error until the website is back online.
        cursor.execute("UPDATE websites SET last_try_failed=1 WHERE url='{}'".format(url))
        conn.commit()

  # Wait for five minutes before checking again
  time.sleep(pollSpeed)