html_content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Social Media Hub - 管理控制台</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 1400px; margin: 0 auto; }
        .header { background: white; border-radius: 10px; padding: 30px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .header h1 { color: #667eea; margin-bottom: 10px; }
        h2 { color: #333; margin-bottom: 20px; padding-bottom: 10px; border-bottom: 2px solid #667eea; }
        .panel { background: white; border-radius: 10px; padding: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
        button { padding: 12px 20px; border: none; border-radius: 6px; font-size: 14px; font-weight: 600; cursor: pointer; color: white; width: 100%; margin-top: 10px; }
        .btn-primary { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        input, select { width: 100%; padding: 12px; border: 2px solid #e5e7eb; border-radius: 6px; margin-top: 8px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1> Social Media Hub 管理控制台</h1>
            <p>Instagram视频自动化处理与B站上传系统</p>
        </div>
        <div class="panel">
            <h2> 快速开始</h2>
            <p>选择账户：</p>
            <select id="account">
                <option value="ai_vanvan">ai_vanvan</option>
                <option value="aigf8728">aigf8728</option>
            </select>
            <button class="btn-primary" onclick="alert('功能开发中...')">开始测试</button>
        </div>
    </div>
</body>
</html>'''

with open('containers/api-gateway/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
print(' index.html created')
