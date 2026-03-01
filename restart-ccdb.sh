#!/bin/bash
#
# Restart Close Call Database (CCDB) service only.
# Keeps other services (RoadWise, Games, K360, Cloudflare) running.
#

set -Eeuo pipefail

CCDB_ROOT="/home/eezis/code/closecall"
VENV_PATH="$CCDB_ROOT/.venv/bin/activate"
GUNICORN_CMD="gunicorn closecall.wsgi:application --config gunicorn-local.conf.py"
GUNICORN_MATCH="gunicorn .*closecall\.wsgi"
NGINX_CONF="$CCDB_ROOT/nginx/nginx-local-test.conf"
PORT_GUNICORN=8890
PORT_NGINX=8888
LOCAL_NGINX_STARTED=0

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_step() { echo ""; echo "$1"; }

port_listening() {
    local port="$1"
    if command -v netstat >/dev/null 2>&1; then
        if netstat -tln 2>/dev/null | awk -v port="$port" '
            NR > 2 {
                n = split($4, parts, ":")
                if (parts[n] == port) { exit 0 }
            }
            END { exit 1 }'
        then
            return 0
        fi
    fi

    if command -v lsof >/dev/null 2>&1 && lsof -ti:"$port" >/dev/null 2>&1; then
        return 0
    fi

    return 1
}

wait_for_port() {
    local port=$1
    local state=$2  # up|down
    local retries=20

    for ((i=1; i<=retries; i++)); do
        if port_listening "$port"; then
            [ "$state" == "up" ] && return 0
        else
            [ "$state" == "down" ] && return 0
        fi
        sleep 0.5
    done

    echo -e "${RED}✗ Port $port did not go ${state} in time${NC}"
    return 1
}

stop_gunicorn() {
    log_step "Step 1: Stopping CCDB Gunicorn (port $PORT_GUNICORN)..."
    local pids
    pids=$(pgrep -f "$GUNICORN_MATCH" || true)
    if [ -n "$pids" ]; then
        echo "  Stopping PIDs: $pids"
        pkill -f "$GUNICORN_MATCH" || true
        wait_for_port "$PORT_GUNICORN" down || {
            echo "  Force killing residual PIDs on port $PORT_GUNICORN"
            lsof -ti:"$PORT_GUNICORN" | xargs -r kill -9
            wait_for_port "$PORT_GUNICORN" down
        }
        echo -e "  ${GREEN}✓${NC} Gunicorn stopped"
    else
        echo -e "  ${YELLOW}⚠${NC} Gunicorn was not running"
    fi
}

stop_nginx() {
    log_step "Step 2: Stopping CCDB Nginx (port $PORT_NGINX)..."
    if pgrep -f "nginx.*nginx-local-test.conf" >/dev/null 2>&1; then
        nginx -c "$NGINX_CONF" -s quit || true
        wait_for_port "$PORT_NGINX" down || {
            echo "  Force killing residual PIDs on port $PORT_NGINX"
            lsof -ti:"$PORT_NGINX" | xargs -r kill -9
            wait_for_port "$PORT_NGINX" down
        }
        echo -e "  ${GREEN}✓${NC} Nginx stopped"
    else
        echo -e "  ${YELLOW}⚠${NC} Nginx was not running"
    fi
}

start_services() {
    log_step "Step 3: Starting CCDB services..."
    cd "$CCDB_ROOT"
    source "$VENV_PATH"

    echo "  Starting Gunicorn [CC] (port $PORT_GUNICORN)..."
    eval "$GUNICORN_CMD" > >(
        sed 's/^/[CC] /'
    ) 2>&1 &
    GUNICORN_PID=$!
    
    if port_listening "$PORT_NGINX"; then
        echo "  Detected another nginx bound to port $PORT_NGINX (likely production); skipping local nginx start."
        LOCAL_NGINX_STARTED=0
        NGINX_PID=""
    else
        echo "  Starting Nginx [CC] (port $PORT_NGINX, foreground)..."
        nginx -c "$NGINX_CONF" -g 'daemon off;' > >(
            sed 's/^/[CC] /'
        ) 2>&1 &
        NGINX_PID=$!
        LOCAL_NGINX_STARTED=1
    fi

    deactivate

    wait_for_port "$PORT_GUNICORN" up
    if [[ $LOCAL_NGINX_STARTED -eq 1 ]]; then
        wait_for_port "$PORT_NGINX" up
    fi
}

verify_services() {
    log_step "Step 4: Verifying services..."
    port_listening "$PORT_GUNICORN" && \
        echo -e "  ${GREEN}✓${NC} Gunicorn is running on port $PORT_GUNICORN" || \
        echo -e "  ${RED}✗${NC} Gunicorn failed to start"

    port_listening "$PORT_NGINX" && \
        echo -e "  ${GREEN}✓${NC} Nginx is running on port $PORT_NGINX" || \
        echo -e "  ${RED}✗${NC} Nginx failed to start"

    echo ""
    echo "Verifying other services are still running:"
    lsof -ti:9988 >/dev/null 2>&1 && echo -e "  ${GREEN}✓${NC} RoadWise MVP (9988)" || echo -e "  ${YELLOW}⚠${NC} RoadWise MVP not running (9988)"
    lsof -ti:7373 >/dev/null 2>&1 && echo -e "  ${GREEN}✓${NC} Games server (7373)" || echo -e "  ${YELLOW}⚠${NC} Games server not running (7373)"
    lsof -ti:7788 >/dev/null 2>&1 && echo -e "  ${GREEN}✓${NC} K360 POC (7788)" || echo -e "  ${YELLOW}⚠${NC} K360 POC not running (7788)"
    pgrep -f "cloudflared tunnel" >/dev/null && echo -e "  ${GREEN}✓${NC} Cloudflare tunnel" || echo -e "  ${YELLOW}⚠${NC} Cloudflare tunnel not running"
}

cleanup() {
    echo ""
    echo "Stopping CCDB services..."
    kill "$GUNICORN_PID" 2>/dev/null || true
    if [[ $LOCAL_NGINX_STARTED -eq 1 && -n "${NGINX_PID:-}" ]]; then
        kill "$NGINX_PID" 2>/dev/null || true
    fi
    wait || true
    echo "CCDB stopped."
}

echo "========================================"
echo "Restarting Close Call Database (CCDB)"
echo "========================================"

# ── Step 0: Preflight checks (BEFORE touching the running server) ──
log_step "Step 0: Running preflight checks..."
PREFLIGHT_SCRIPT="$CCDB_ROOT/preflight-check.sh"
if [[ -x "$PREFLIGHT_SCRIPT" ]]; then
    if ! "$PREFLIGHT_SCRIPT"; then
        echo -e "${RED}✗ Preflight failed — aborting restart. Running server was NOT touched.${NC}"
        exit 1
    fi
    echo -e "  ${GREEN}✓${NC} Preflight passed"
else
    echo -e "  ${YELLOW}⚠${NC} preflight-check.sh not found or not executable — skipping"
fi

stop_gunicorn
stop_nginx
start_services
verify_services

echo ""
echo "Checking public site reachability..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 https://closecalldatabase.com || echo "000")
if [[ "$HTTP_CODE" =~ ^(2|3) ]]; then
    echo -e "  ${GREEN}The site is in PRODUCTION (HTTP $HTTP_CODE)${NC}"
else
    echo -e "  ${RED}ERROR ERROR ERROR  THE SITE DID NOT START  (HTTP $HTTP_CODE)  ERROR ERROR ERROR${NC}"
fi

echo ""
completion_ts="$(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================="
echo -e "${GREEN}✓ CCDB restart complete!${NC}  ${completion_ts}"
echo "========================================="
echo ""
echo "CCDB is now available at:"
echo "  • Nginx (local):  http://localhost:${PORT_NGINX}"
echo "  • Gunicorn:       http://localhost:${PORT_GUNICORN}"
echo "  • Public URL:     https://closecalldatabase.com (via Cloudflare)"
echo ""
echo "=== [CC] logs will appear below ==="
echo "Press Ctrl+C to stop CCDB services"
echo ""

trap cleanup SIGINT SIGTERM
wait
