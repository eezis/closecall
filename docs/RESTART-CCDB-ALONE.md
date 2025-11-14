
## Restarting CCDB Only

Open a new terminal and run the tracked helper from the repo root (it handles the
virtualenv, skips nginx if production already owns :8888, and performs a curl
health check against the public site):

```bash
cd /home/eezis/code/closecall
./restart-ccdb.sh
```

Watch the output for:

* green checks on Gunicorn and Nginx
* `The site is in PRODUCTION (HTTP 200)` after the curl
* the banner + “[CC] logs will appear below” block

Finally, hit https://closecalldatabase.com in a browser to confirm.

## If CCDB Still Misbehaves

1. **Reload Cloudflare tunnel config** (no downtime for other services):
   ```bash
   pkill -HUP cloudflared
   ```
2. **Restart only the tunnel** (brief downtime for everything):
   ```bash
   pkill cloudflared
   ```
   Then relaunch via whatever supervisor/systemd unit you normally use.
3. **Full stack restart (last resort)**:
   ```bash
   ./stop_all_services.sh
   ./start_all_services_with_prefixes.sh   # run this where you want to see logs
   ```

Re-test CCDB and the companion services after each step.

## Investigating Tunnel Issues

Tail the Cloudflare logs:

```bash
tail -f /home/eezis/.cloudflared/cloudflared.log
```
