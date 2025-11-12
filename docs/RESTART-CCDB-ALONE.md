
go to a new terminal and run:

```
cd ~
./restart-ccdb.sh
```

test http://closecalldatabase.com to confirm everything is working.


if it is not try:

  2. Reload tunnel config (no downtime for other services)

  # Send HUP signal to reload without full restart
  pkill -HUP cloudflared

  3. Restart just the tunnel (brief downtime for ALL services)

  # Kill the tunnel
  pkill cloudflared



Remember to retest ccdb and the other services.


If still a problem,

./stop_all_services.sh

then in the terminal where you wish to observe logs,

./start_all_services_with_prefixes.sh


Then test all services again.


To investigate CloudFlare tunnel issues,

then check logs:

  # Check cloudflared logs
  tail -f /home/eezis/.cloudflared/cloudflared.log
