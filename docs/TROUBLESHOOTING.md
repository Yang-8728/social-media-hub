# Troubleshooting Guide

## 🐛 Common Issues

### Unicode Path Problems
**Problem**: Windows path separator confusion (﹨ vs \)
**Solution**: 
- Use raw strings: `r"path\to\file"`
- Normalize paths with `os.path.normpath()`
- Check encoding with `sys.getfilesystemencoding()`

### Download Detection Issues
**Problem**: Downloads not detected properly
**Solution**:
- Verify timestamp checking logic
- Clear browser cache
- Check file permissions

### Upload Failures
**Problem**: B站上传失败
**Solution**:
- Check login status
- Verify video format (MP4 recommended)
- Ensure stable internet connection
- Check category selection logic

### Chrome Driver Issues
**Problem**: WebDriver crashes or timeouts
**Solution**:
- Update Chrome and ChromeDriver versions
- Clear browser data
- Check for popup blockers
- Verify profile settings

## 🔧 Debug Commands

```bash
# Check system status
python main.py --status

# Verify file integrity  
python main.py --check-files

# Test upload without actual submission
python main.py --test-upload path/to/video.mp4
```

## 📞 Getting Help

1. Check logs in `logs/` directory
2. Run with `--verbose` flag for detailed output
3. Verify configuration in `config/accounts.json`
