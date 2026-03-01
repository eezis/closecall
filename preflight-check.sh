#!/bin/bash
#
# Pre-deploy safety checks for Close Call Database (CCDB).
#
# Catches SyntaxErrors, smart-quote typos, broken Django config,
# and bad Gunicorn settings BEFORE the running server is touched.
#
# Usage:
#   ./preflight-check.sh          # run all checks
#   ./preflight-check.sh --quick  # skip Django/Gunicorn (syntax only)
#
# Exit codes:
#   0  All checks passed
#   1  One or more checks failed — do NOT deploy
#

set -euo pipefail

CCDB_ROOT="$(cd "$(dirname "$0")" && pwd)"
VENV_PATH="$CCDB_ROOT/.venv/bin/activate"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

FAILURES=0
QUICK=0

[[ "${1:-}" == "--quick" ]] && QUICK=1

fail() {
    echo -e "  ${RED}FAIL${NC}: $1"
    FAILURES=$((FAILURES + 1))
}

pass() {
    echo -e "  ${GREEN}OK${NC}: $1"
}

# Directories containing our application code (skip legacy/vendor dirs)
APP_DIRS=(core incident users publish api closecall tests)

echo ""
echo "═══════════════════════════════════════"
echo "  CCDB Pre-Deploy Preflight Checks"
echo "═══════════════════════════════════════"
echo ""

# ── Check 1: Python syntax (compileall) ──────────────────────────
echo "1/4  Python syntax (compileall)..."

COMPILE_ERRORS=""
for dir in "${APP_DIRS[@]}"; do
    target="$CCDB_ROOT/$dir"
    [[ -d "$target" ]] || continue
    output=$(python3 -m compileall -q "$target" 2>&1) || {
        COMPILE_ERRORS+="$output"$'\n'
    }
done

if [[ -n "$COMPILE_ERRORS" ]]; then
    fail "SyntaxError(s) found in application code"
    echo "$COMPILE_ERRORS" | head -20
else
    pass "All .py files compile cleanly"
fi

# ── Check 2: Unicode smart quotes ────────────────────────────────
echo "2/4  Unicode smart quotes in .py files..."

SMART_QUOTE_HITS=""
for dir in "${APP_DIRS[@]}"; do
    target="$CCDB_ROOT/$dir"
    [[ -d "$target" ]] || continue
    # U+2018 ' U+2019 ' U+201C " U+201D "
    hits=$(grep -rnP '[\x{2018}\x{2019}\x{201C}\x{201D}]' "$target"/*.py "$target"/**/*.py 2>/dev/null || true)
    if [[ -n "$hits" ]]; then
        SMART_QUOTE_HITS+="$hits"$'\n'
    fi
done

if [[ -n "$SMART_QUOTE_HITS" ]]; then
    fail "Unicode smart quotes found (replace with ASCII quotes)"
    echo "$SMART_QUOTE_HITS" | head -20
else
    pass "No smart quotes detected"
fi

if [[ $QUICK -eq 1 ]]; then
    echo ""
    echo "3/4  Django system check... SKIPPED (--quick)"
    echo "4/4  Gunicorn config...     SKIPPED (--quick)"
else
    # ── Check 3: Django system check ─────────────────────────────────
    echo "3/4  Django system check..."

    source "$VENV_PATH"
    cd "$CCDB_ROOT"

    django_output=$(python manage.py check 2>&1) && {
        pass "Django system check passed"
    } || {
        fail "Django system check failed"
        echo "$django_output" | head -20
    }

    # ── Check 4: Gunicorn config ─────────────────────────────────────
    echo "4/4  Gunicorn config validation..."

    gunicorn_output=$(gunicorn --check-config closecall.wsgi:application --config gunicorn-local.conf.py 2>&1) && {
        pass "Gunicorn config is valid"
    } || {
        fail "Gunicorn config check failed"
        echo "$gunicorn_output" | head -20
    }

    deactivate 2>/dev/null || true
fi

# ── Summary ──────────────────────────────────────────────────────
echo ""
if [[ $FAILURES -gt 0 ]]; then
    echo -e "${RED}═══════════════════════════════════════${NC}"
    echo -e "${RED}  PREFLIGHT FAILED  ($FAILURES check(s))${NC}"
    echo -e "${RED}  DO NOT DEPLOY${NC}"
    echo -e "${RED}═══════════════════════════════════════${NC}"
    exit 1
else
    echo -e "${GREEN}═══════════════════════════════════════${NC}"
    echo -e "${GREEN}  ALL PREFLIGHT CHECKS PASSED${NC}"
    echo -e "${GREEN}═══════════════════════════════════════${NC}"
    exit 0
fi
