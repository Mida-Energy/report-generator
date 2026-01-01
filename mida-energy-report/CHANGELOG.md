# Changelog

All notable changes to the Energy Reports add-on will be documented in this file.

## [1.0.6] - 2025-12-31

### Added
- Automatic Shelly device discovery from Home Assistant
- Background data collection with configurable intervals
- Manual data collection button in web interface
- Reports now saved to `/media/energy_reports` for easy access
- Enhanced web UI with detailed status messages
- Comprehensive logging with visual indicators
- Direct download link appears after report generation

### Changed
- Renamed from "Mida Energy Report Generator" to "Energy Reports"
- Changed default paths to use `energy_reports` naming
- Migrated to Alpine-based image for better performance
- Improved permissions handling for container execution
- Updated panel icon to chart-line for better representation

### Fixed
- Fixed permission denied errors on entrypoint execution
- Resolved AppArmor conflicts with init system
- Corrected CSV file path handling

## [1.0.5] - 2025-12-30

### Initial Release
- First version of the add-on
- Basic PDF report generation
- Manual CSV data processing
- Flask-based web interface

---

## Future Plans

- [ ] Configurable entity selection in UI
- [ ] Multiple report templates
- [ ] Email report delivery
- [ ] Historical data comparison
- [ ] Cost calculation features
- [ ] Multi-language support
