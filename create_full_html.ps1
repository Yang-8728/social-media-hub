$html = @"
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Social Media Hub - 管理控制台</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 1400px; margin: 0 auto; }
        .header { background: white; border-radius: 10px; padding: 30px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .header h1 { color: #667eea; margin-bottom: 10px; }
        .main-content { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
        @media (max-width: 1024px) { .main-content { grid-template-columns: 1fr; } }
        .panel { background: white; border-radius: 10px; padding: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .panel h2 { color: #333; margin-bottom: 20px; padding-bottom: 10px; border-bottom: 2px solid #667eea; }
        .control-group { margin-bottom: 20px; }
        .control-group label { display: block; margin-bottom: 8px; color: #555; font-weight: 500; }
        .control-group input, .control-group select { width: 100%; padding: 12px; border: 2px solid #e5e7eb; border-radius: 6px; font-size: 14px; }
        .button-group { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-top: 20px; }
        button { padding: 12px 20px; border: none; border-radius: 6px; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.3s; color: white; }
        button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
        .btn-primary { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .btn-success { background: linear-gradient(135deg, #10b981 0%, #059669 100%); }
        .btn-info { background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); }
        .btn-warning { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); }
        .btn-danger { background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); }
        .btn-secondary { background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%); }
        .log-panel { grid-column: 1 / -1; }
        .log-container { background: #1e1e1e; border-radius: 6px; padding: 15px; height: 400px; overflow-y: auto; font-family: 'Courier New', monospace; font-size: 13px; }
        .log-entry { margin-bottom: 8px; padding: 5px; border-left: 3px solid transparent; }
        .log-entry.info { color: #3b82f6; border-left-color: #3b82f6; }
        .log-entry.success { color: #10b981; border-left-color: #10b981; }
        .log-entry.warning { color: #f59e0b; border-left-color: #f59e0b; }
        .log-entry.error { color: #ef4444; border-left-color: #ef4444; }
        .log-time { color: #9ca3af; margin-right: 10px; }
        .toast { position: fixed; top: 20px; right: 20px; padding: 15px 20px; border-radius: 8px; color: white; font-weight: 500; box-shadow: 0 4px 12px rgba(0,0,0,0.15); z-index: 1000; }
        .toast.success { background: #10b981; }
        .toast.error { background: #ef4444; }
        .toast.info { background: #3b82f6; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1> Social Media Hub 管理控制台</h1>
            <p>Instagram视频自动化处理与B站上传系统</p>
        </div>
        <div class="main-content">
            <div class="panel">
                <h2> 账户认证</h2>
                <div class="control-group">
                    <label>Instagram账户</label>
                    <select id="account-select">
                        <option value="ai_vanvan">ai_vanvan</option>
                        <option value="aigf8728">aigf8728</option>
                    </select>
                </div>
                <div class="button-group">
                    <button class="btn-primary" onclick="runAuth()"> 登录认证</button>
                    <button class="btn-secondary" onclick="checkAuthStatus()"> 检查状态</button>
                </div>
            </div>
            <div class="panel">
                <h2> 扫描新内容</h2>
                <div class="control-group">
                    <label>扫描限制（帖子数）</label>
                    <input type="number" id="scan-limit" value="50" min="1" max="200">
                </div>
                <div class="button-group">
                    <button class="btn-success" onclick="runScanner()"> 开始扫描</button>
                    <button class="btn-secondary"> 查看结果</button>
                </div>
            </div>
            <div class="panel">
                <h2> 下载视频</h2>
                <div class="control-group">
                    <label>下载数量限制</label>
                    <input type="number" id="download-limit" value="10" min="1" max="50">
                </div>
                <div class="button-group">
                    <button class="btn-info" onclick="runDownloader()"> 开始下载</button>
                    <button class="btn-secondary"> 查看下载</button>
                </div>
            </div>
            <div class="panel">
                <h2> 标准化处理</h2>
                <div class="control-group">
                    <label>目标分辨率</label>
                    <select id="resolution">
                        <option value="720x1280">720x1280 (竖屏HD)</option>
                        <option value="1080x1920">1080x1920 (竖屏FHD)</option>
                    </select>
                </div>
                <div class="button-group">
                    <button class="btn-warning" onclick="runStandardizer()"> 标准化处理</button>
                    <button class="btn-secondary"> 处理状态</button>
                </div>
            </div>
            <div class="panel">
                <h2> 合并视频</h2>
                <div class="control-group">
                    <label>合并视频数量</label>
                    <input type="number" id="merge-count" value="15" min="1" max="30">
                </div>
                <div class="button-group">
                    <button class="btn-primary" onclick="runMerger()"> 开始合并</button>
                    <button class="btn-secondary"> 查看合并</button>
                </div>
            </div>
            <div class="panel">
                <h2> B站上传</h2>
                <div class="control-group">
                    <label>选择视频文件</label>
                    <select id="video-select">
                        <option value="latest">最新合并视频</option>
                    </select>
                </div>
                <div class="button-group">
                    <button class="btn-danger" onclick="runUploader()"> 上传到B站</button>
                    <button class="btn-secondary"> 上传历史</button>
                </div>
            </div>
            <div class="panel log-panel">
                <h2> 实时日志</h2>
                <div class="log-container" id="log-container">
                    <div class="log-entry info"><span class="log-time">[00:00:00]</span>系统初始化完成，等待操作...</div>
                </div>
            </div>
        </div>
    </div>
    <script>
        function addLog(msg, type = 'info') {
            const log = document.getElementById('log-container');
            const time = new Date().toTimeString().split(' ')[0];
            const entry = document.createElement('div');
            entry.className = `log-entry ${type}`;
            entry.innerHTML = `<span class="log-time">[${time}]</span>${msg}`;
            log.appendChild(entry);
            log.scrollTop = log.scrollHeight;
        }
        function showToast(msg, type = 'info') {
            const toast = document.createElement('div');
            toast.className = `toast ${type}`;
            toast.textContent = msg;
            document.body.appendChild(toast);
            setTimeout(() => toast.remove(), 3000);
        }
        async function callAPI(endpoint, data) {
            try {
                const res = await fetch(endpoint, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                return await res.json();
            } catch(e) {
                return {status: 'error', error: e.message};
            }
        }
        async function runAuth() {
            const account = document.getElementById('account-select').value;
            addLog(`正在进行账户认证: ${account}...`, 'info');
            const result = await callAPI('/api/auth/login', {account});
            if(result.status === 'success') {
                addLog(` 账户认证成功: ${account}`, 'success');
                showToast('账户认证成功！', 'success');
            } else {
                addLog(` 认证失败: ${result.error}`, 'error');
                showToast('认证失败', 'error');
            }
        }
        async function checkAuthStatus() {
            const account = document.getElementById('account-select').value;
            addLog(`检查账户状态: ${account}...`, 'info');
            const result = await fetch(`/api/auth/status/${account}`).then(r=>r.json());
            addLog(`账户状态: ${result.authenticated ? '已认证' : '未认证'}`, 'info');
        }
        async function runScanner() {
            const account = document.getElementById('account-select').value;
            const limit = document.getElementById('scan-limit').value;
            addLog(`开始扫描账户 ${account}，限制 ${limit} 个帖子...`, 'info');
            const result = await callAPI('/api/scanner/scan', {account, limit: parseInt(limit)});
            if(result.status === 'success') {
                addLog(` 扫描任务已创建`, 'success');
                showToast('扫描任务已创建！', 'success');
            } else {
                addLog(` 扫描失败: ${result.error}`, 'error');
                showToast('扫描失败', 'error');
            }
        }
        async function runDownloader() {
            const account = document.getElementById('account-select').value;
            const limit = document.getElementById('download-limit').value;
            addLog(`开始下载视频，限制 ${limit} 个...`, 'info');
            const result = await callAPI('/api/downloader/download', {account, max_downloads: parseInt(limit)});
            if(result.status === 'success') {
                addLog(` 下载任务已创建`, 'success');
                showToast('下载任务已创建！', 'success');
            } else {
                addLog(` 下载失败: ${result.error}`, 'error');
                showToast('下载失败', 'error');
            }
        }
        async function runStandardizer() {
            const account = document.getElementById('account-select').value;
            const resolution = document.getElementById('resolution').value;
            addLog(`开始标准化处理，目标分辨率: ${resolution}...`, 'info');
            const result = await callAPI('/api/standardizer/process', {account, resolution});
            if(result.status === 'success') {
                addLog(` 标准化任务已创建`, 'success');
                showToast('标准化任务已创建！', 'success');
            } else {
                addLog(` 标准化失败: ${result.error}`, 'error');
                showToast('标准化失败', 'error');
            }
        }
        async function runMerger() {
            const account = document.getElementById('account-select').value;
            const count = document.getElementById('merge-count').value;
            addLog(`开始合并视频，数量: ${count}...`, 'info');
            const result = await callAPI('/api/merger/merge', {account, limit: parseInt(count)});
            if(result.status === 'success') {
                addLog(` 合并任务已创建`, 'success');
                showToast('合并任务已创建！', 'success');
            } else {
                addLog(` 合并失败: ${result.error}`, 'error');
                showToast('合并失败', 'error');
            }
        }
        async function runUploader() {
            if(!confirm('确定要上传视频到B站吗？')) return;
            const account = document.getElementById('account-select').value;
            addLog(`准备上传视频到B站...`, 'info');
            const result = await callAPI('/api/uploader/upload', {account, video_path: null});
            if(result.status === 'success') {
                addLog(` 上传任务已创建`, 'success');
                showToast('上传任务已创建！', 'success');
            } else {
                addLog(` 上传失败: ${result.error}`, 'error');
                showToast('上传失败', 'error');
            }
        }
    </script>
</body>
</html>
"@

$html | Out-File -FilePath "containers\api-gateway\templates\index.html" -Encoding UTF8
Write-Host " 完整版index.html已创建"
