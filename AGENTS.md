# Repository Guidelines

## Project Structure & Module Organization
Core Django config sits in `closecall/` with `settings.py`, `urls.py`, and `wsgi.py`. Feature apps (`core`, `incident`, `users`, `api`, `geoposition`, `utils`) hold business logic, while templates live in `templates/` with static assets under `static/` and deploy bundles in `nginx-root/static/`. Python suites live in `tests/` plus root-level `test_*.py`.

## Build, Test, and Development Commands
Install deps via `uv pip install -r requirements.txt`, then run `python manage.py makemigrations`, `python manage.py migrate`, and `python manage.py collectstatic --noinput`. Use `python manage.py runserver 0.0.0.0:8000` only for local debugging; production entry still flows through Gunicorn. Run `python manage.py test tests` or targeted modules (e.g., `tests.test_authentication`), and execute `npm install && node test_strava_button.js` for Puppeteer checks.

## Service Operations & Cloudflare Tunnel
This machine is a live production host exposed through Cloudflare Tunnels (config in `cloudflare/config.yml`). Traffic path: Internet → Cloudflare Tunnel (`cloudflared`) → Nginx on port 8888 → Gunicorn on port 8890 → Django. Only the user runs `./stop_all_servers.sh` (which shuts down the tunnel, Nginx, Gunicorn, UVicorn, and ancillary Django/FastAPI services) and `./start_all_servers_with_prefixes.sh` (prints the full ingress/port map and starts everything); do not touch those daemons directly.

## Coding Style & Naming Conventions
Use four-space indents, module docstrings, and import groups (stdlib → third-party → project). Favor `snake_case` for functions/vars, `PascalCase` for Django models/forms, and reuse template naming such as `incident/reporting-step-2.html`. Keep config tweaks in `closecall/settings.py` or app `apps.py`, and colocate CSS/JS overrides beside their templates inside `static/`.

## Testing Guidelines
Choose `TestCase` for typical DB isolation and `TransactionTestCase` when `transaction.on_commit` is involved (see `tests/test_authentication.py`). Prefix scenarios with `test_*`, keep fixtures explicit, and rerun Puppeteer whenever Strava or login UI changes. The local PostgreSQL instance is the production database—never run tests or destructive commands against it; use mocks, SQLite, or read-only diagnostics unless the user explicitly provisions a dev DB.

## Commit & Pull Request Guidelines
Recent commits look like “Fix contact form spam detection to log real client IP,” so keep messages imperative, ≤72 chars, and add body context when motivation is non-obvious. PRs need a short impact summary, referenced issues/incidents, screenshots for template/UI edits, and an explicit list of commands/tests executed.

## Security & Configuration Tips
Keep secrets in `.env` (gitignored) and document new environment values in `CLAUDE.md` so future agents stay aligned. Never touch `nginx/`, `systemd/`, or tunnel configs without owner approval, and assume PostgreSQL (`closecall` / `eaecc`) is the source of truth—SQLite behavior is non-binding. Validate migrations against that stack before asking the user to run the production start/stop scripts.
