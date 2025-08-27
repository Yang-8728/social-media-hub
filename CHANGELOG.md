# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Complete project structure reorganization
- Comprehensive README documentation for all major directories
- Unicode path bug fixing system
- Intelligent video merger with resolution normalization
- Automated file migration tools

### Fixed
- Critical Unicode path separator bug (﹨ vs \) in Windows
- Download detection logic using timestamp verification
- File location confusion in mixed Unicode/standard paths

### Changed
- Moved 30+ legacy Python files to cleanup_old_files/ directory
- Reorganized tools into tools/setup/ and tools/scripts/ structure
- Enhanced .gitignore to properly exclude large FFmpeg tools and media files

## [0.1.0] - 2025-08-27

### Added
- Initial project structure
- Instagram downloader functionality
- Basic video merging capabilities
- Multi-account support
- Logging system

### Technical Details
- Python 3.11.9 support
- FFmpeg integration for video processing
- Comprehensive error handling
- Unicode path compatibility

---

## Version History Summary

- **v0.1.0** (2025-08-27): Initial release with core functionality
- **Unreleased**: Major structure reorganization and Unicode bug fixes

## Migration Notes

If upgrading from earlier versions:
1. Run `tools/scripts/fix_unicode_paths.py` to migrate any files in Unicode paths
2. Update any custom scripts to use the new directory structure
3. Check that FFmpeg tools are properly extracted in `tools/ffmpeg/`

## Contributors

- Yang-8728 - Initial development and maintenance

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
