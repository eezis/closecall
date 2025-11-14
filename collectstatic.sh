#!/bin/bash
#
# Collect Django static assets and deploy them to the nginx document root.
#

set -Eeuo pipefail

PROJECT_ROOT="/home/eezis/code/closecall"
VENV_PATH="$PROJECT_ROOT/.venv/bin/activate"
DJANGO_MANAGE="python manage.py"
COLLECTED_STATIC_DIR="$PROJECT_ROOT/staticfiles"
NGINX_STATIC_DIR="$PROJECT_ROOT/nginx-root/static"
VENV_WAS_ACTIVATED=0

log() { printf '\n[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"; }

activate_venv() {
    if [[ -z "${VIRTUAL_ENV:-}" ]]; then
        if [[ -f "$VENV_PATH" ]]; then
            # shellcheck disable=SC1090
            source "$VENV_PATH"
            VENV_WAS_ACTIVATED=1
        else
            echo "Virtualenv not found at $VENV_PATH" >&2
            exit 1
        fi
    fi
}

deactivate_venv() {
    if [[ $VENV_WAS_ACTIVATED -eq 1 ]]; then
        deactivate
    fi
}

run_collectstatic() {
    log "Running manage.py collectstatic"
    cd "$PROJECT_ROOT"
    $DJANGO_MANAGE collectstatic --noinput
}

sync_to_nginx() {
    log "Deploying collected assets to nginx-root/static"
    mkdir -p "$NGINX_STATIC_DIR"
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "$COLLECTED_STATIC_DIR"/ "$NGINX_STATIC_DIR"/
    else
        rm -rf "$NGINX_STATIC_DIR"
        mkdir -p "$NGINX_STATIC_DIR"
        cp -a "$COLLECTED_STATIC_DIR"/. "$NGINX_STATIC_DIR"/
    fi
}

main() {
    log "Starting collectstatic deployment"
    activate_venv
    trap deactivate_venv EXIT

    run_collectstatic
    sync_to_nginx

    log "Static assets collected and copied to nginx-root/static"
}

main "$@"
