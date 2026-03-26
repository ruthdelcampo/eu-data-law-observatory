#!/usr/bin/env bash
#
# Fetch a law's HTML from EUR-Lex and save to raw/
#
# Usage: ./scripts/fetch-law.sh <CELEX_NUMBER> <output_path>
# Example: ./scripts/fetch-law.sh 32016R0679 eu-wide/gdpr
#
# This downloads the English HTML version of the law and saves it to:
#   raw/<output_path>.html
#
# NOTE: EUR-Lex uses AWS WAF protection that may block automated requests.
# If this script fails with HTTP 202, use browser-based fetching instead
# (e.g., Claude Code's Chrome automation tools or manual download).

set -euo pipefail

if [ $# -ne 2 ]; then
    echo "Usage: $0 <CELEX_NUMBER> <output_path>"
    echo "Example: $0 32016R0679 eu-wide/gdpr"
    exit 1
fi

CELEX="$1"
OUTPUT_PATH="$2"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

OUTPUT_FILE="$PROJECT_ROOT/raw/${OUTPUT_PATH}.html"
OUTPUT_DIR="$(dirname "$OUTPUT_FILE")"

URL="https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:${CELEX}"

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

echo "Fetching: $URL"
echo "Saving to: $OUTPUT_FILE"

MAX_RETRIES=3
RETRY_DELAY=3

for attempt in $(seq 1 $MAX_RETRIES); do
    HTTP_CODE=$(curl -s -o "$OUTPUT_FILE" -w "%{http_code}" -L \
        -H "Accept: text/html" \
        -H "User-Agent: EU-Data-Law-Observatory/1.0" \
        "$URL")

    if [ "$HTTP_CODE" -eq 200 ]; then
        break
    fi

    if [ "$attempt" -lt "$MAX_RETRIES" ]; then
        echo "Attempt $attempt: HTTP $HTTP_CODE — retrying in ${RETRY_DELAY}s..."
        sleep "$RETRY_DELAY"
    else
        echo "Error: HTTP $HTTP_CODE after $MAX_RETRIES attempts — failed to fetch CELEX $CELEX"
        rm -f "$OUTPUT_FILE"
        exit 1
    fi
done

FILE_SIZE=$(wc -c < "$OUTPUT_FILE" | tr -d ' ')
echo "Downloaded: ${FILE_SIZE} bytes"
echo "Done. Update registry.yaml observatory_status to 'collected'."
