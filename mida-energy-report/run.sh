#!/usr/bin/with-contenv bashio
# ==============================================================================
# Start Mida Energy Report Generator Add-on
# ==============================================================================

bashio::log.info "Starting Mida Energy Report Generator..."

# Read configuration from add-on options
DATA_PATH=$(bashio::config 'data_path')
AUTO_EXPORT=$(bashio::config 'auto_export_enabled')
EXPORT_INTERVAL=$(bashio::config 'export_interval_hours')

bashio::log.info "Data path: ${DATA_PATH}"
bashio::log.info "Auto export: ${AUTO_EXPORT}"
bashio::log.info "Export interval: ${EXPORT_INTERVAL} hours"

# Create data directory if it doesn't exist
mkdir -p "${DATA_PATH}"
mkdir -p /app/reports/generale

# Set environment variables for the app
export DATA_PATH="${DATA_PATH}"
export AUTO_EXPORT="${AUTO_EXPORT}"
export EXPORT_INTERVAL="${EXPORT_INTERVAL}"

bashio::log.info "Starting API server on port 5000..."

# Start the Flask API server
cd /app
exec gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 300 --access-logfile - app:app
