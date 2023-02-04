# Python3 Web Poller - Check for downtime!

## Requirements
- Python3
- pip(3) (+packages:)
    - `pip install requests`
    - `pip install mysql-connector-python`
    - `pip install python-dotenv`
- MariaDB / MySQL database that the server can reach.
- A Discord webhook url.

## Instructions

### Set-up

- Create a database for the script
- Migrate the `Migrations/web_monitor.sql` file to the database.
- Add the websites that you want to monitor the in the `websites`
- Copy `.env.example` to `.env` file and configure it.\
- Run the script & enjoy :).
- It's preferred to run the script as a service.

### Service file example

The location where you save the systemd service file depends on the operating system you're using. In most cases, service files are saved in the `/etc/systemd/system/` directory.

For example, if your service file is named `myscript.service`, you would save it as `/etc/systemd/system/myscript.service`.

Once you've saved the service file, you can use the systemctl command to start, stop, restart, and check the status of your service. For example, to start the service, you can run: `sudo systemctl start myscript.service
`.

The following script is an example of how to run the `web_monitor_py.py` as a service.

*Note that you'll need to replace `/path/to/` with the actual path to your script and myuser and mygroup with the correct values for your system.*

```ini
[Unit]
Description=Python3 Web Poller to check for online status and send a Discord notification on bad statuses.

[Service]
ExecStart=/usr/bin/python3 /path/to/web_monitor_py.py
WorkingDirectory=/path/to/
User=myuser
Group=mygroup
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

- `Description`: A human-readable description of the service.
- `ExecStart`: The command to run when starting the service, which in this case is /usr/bin/python3 and the path to the script.
- `WorkingDirectory`: The directory where the script is located, which will also be set as the current working directory when the script is run.
- `User`: The user that the service should run as.
- `Group`: The group that the service should run as.
- `Restart`: The conditions under which the service should be automatically restarted. In this case, it will restart only when it fails (i.e., exits with a non-zero status).
- `WantedBy`: The target unit this unit should be started when activated.
