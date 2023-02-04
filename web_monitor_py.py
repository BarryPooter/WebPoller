import mysql.connector
import requests
import time
import os

# Connect to the MySQL database
conn = mysql.connector.connect(
  host="host",
  user="user",
  password="password",
  database="database"
)
cursor = conn.cursor()

# Query the database to get the list of websites
query = "SELECT url FROM websites"
cursor.execute(query)
websites = cursor.fetchall()

# Define the Discord webhook URL
discord_webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')

while True:
  for website in websites:
    url = website[0]

    # Check if the website is online
    try:
      response = requests.get(url)
      status = response.status_code
      if status != 200:
        # Send a Discord notification if the website is offline
        discord_message = f"The website {url} is offline. Response code: {status}"
        requests.post(discord_webhook_url, data={"content": discord_message})
    except requests.exceptions.RequestException as e:
      # Send a Discord notification if the website is offline
      discord_message = f"The website {url} is offline. Error: {e}"
      requests.post(discord_webhook_url, data={"content": discord_message})

  # Wait for five minutes before checking again
  time.sleep(300)