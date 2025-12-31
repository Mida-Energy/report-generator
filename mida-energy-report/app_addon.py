"""
Mida Energy Report Generator - Home Assistant Add-on version
Integrated API with automatic Shelly data collection
"""
from flask import Flask, jsonify, send_file, request
from pathlib import Path
import sys
import logging
from datetime import datetime
import os

# Add report generator to path
sys.path.insert(0, str(Path(__file__).parent / 'report_generator' / 'src'))

from main import ShellyEnergyReport

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get paths from environment (set by add-on)
DATA_PATH = Path(os.getenv('DATA_PATH', '/config/mida_energy/data'))
OUTPUT_PATH = Path('/share/mida_energy_reports')
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)


@app.route('/')
def home():
    """Home page with links to all features"""
    return jsonify({
        'status': 'online',
        'service': 'Mida Energy Report Generator',
        'version': '1.0.0',
        'addon': True,
        'endpoints': {
            '/health': 'Health check',
            '/generate': 'Generate PDF report (POST)',
            '/download/latest': 'Download latest PDF',
            '/status': 'Get report status'
        }
    })


@app.route('/health')
def health():
    """Health check for Home Assistant"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})


@app.route('/generate', methods=['POST'])
def generate_report():
    """Generate PDF report from CSV data"""
    try:
        logger.info("=== Starting PDF report generation ===")
        
        # Check data folder
        if not DATA_PATH.exists():
            logger.error(f"Data folder not found: {DATA_PATH}")
            return jsonify({
                'status': 'error',
                'message': f'Data folder not found: {DATA_PATH}'
            }), 404
        
        # Check for CSV files
        csv_files = list(DATA_PATH.glob("*.csv"))
        if not csv_files:
            logger.error("No CSV files found")
            return jsonify({
                'status': 'error',
                'message': 'No CSV files found. Make sure Shelly data is being collected.'
            }), 404
        
        logger.info(f"Found {len(csv_files)} CSV files")
        
        # Create analyzer and generate report
        analyzer = ShellyEnergyReport(
            data_dir=str(DATA_PATH),
            output_dir=str(OUTPUT_PATH.parent),
            correct_timestamps=True
        )
        
        logger.info("Running analysis and generating PDF...")
        analyzer.run_analysis()
        
        # Check if PDF was created
        pdf_file = OUTPUT_PATH / 'report_generale.pdf'
        if pdf_file.exists():
            logger.info(f"PDF generated successfully: {pdf_file}")
            return jsonify({
                'status': 'success',
                'message': 'Report generated successfully!',
                'pdf_size_kb': round(pdf_file.stat().st_size / 1024, 2),
                'timestamp': datetime.now().isoformat(),
                'download_url': '/download/latest'
            })
        else:
            logger.error("PDF not found after generation")
            return jsonify({
                'status': 'error',
                'message': 'PDF generation failed'
            }), 500
            
    except Exception as e:
        logger.error(f"Error generating report: {e}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/download/latest')
def download_latest():
    """Download the latest PDF report"""
    try:
        pdf_file = OUTPUT_PATH / 'report_generale.pdf'
        
        if not pdf_file.exists():
            return jsonify({
                'status': 'error',
                'message': 'No report found. Generate one first.'
            }), 404
        
        # Get file info
        file_stat = pdf_file.stat()
        file_date = datetime.fromtimestamp(file_stat.st_mtime)
        
        logger.info(f"Serving PDF: {pdf_file}")
        
        return send_file(
            pdf_file,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'mida_energy_report_{file_date.strftime("%Y%m%d")}.pdf'
        )
        
    except Exception as e:
        logger.error(f"Error serving PDF: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/status')
def get_status():
    """Get status of reports and data"""
    try:
        pdf_file = OUTPUT_PATH / 'report_generale.pdf'
        
        # Count CSV files
        csv_count = len(list(DATA_PATH.glob("*.csv"))) if DATA_PATH.exists() else 0
        
        if not pdf_file.exists():
            return jsonify({
                'status': 'no_report',
                'has_report': False,
                'csv_files_count': csv_count,
                'data_path': str(DATA_PATH)
            })
        
        # Get PDF info
        file_stat = pdf_file.stat()
        file_date = datetime.fromtimestamp(file_stat.st_mtime)
        
        return jsonify({
            'status': 'ready',
            'has_report': True,
            'last_generated': file_date.isoformat(),
            'last_generated_human': file_date.strftime('%d/%m/%Y %H:%M:%S'),
            'pdf_size_kb': round(file_stat.st_size / 1024, 2),
            'csv_files_count': csv_count,
            'data_path': str(DATA_PATH),
            'download_url': '/download/latest'
        })
        
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


if __name__ == '__main__':
    # Ensure directories exist
    DATA_PATH.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    
    logger.info("Starting Mida Energy Report API (Add-on mode)...")
    logger.info(f"Data path: {DATA_PATH}")
    logger.info(f"Output path: {OUTPUT_PATH}")
    
    # Run server (production mode for add-on)
    app.run(host='0.0.0.0', port=5000, debug=False)
