$html = @"
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Social Media Hub - 管理控制台</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 15px; }
        .container { max-width: 1600px; margin: 0 auto; }
        .header { background: white; border-radius: 8px; padding: 20px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .header h1 { color: #667eea; margin-bottom: 5px; font-size: 24px; }
        .header p { font-size: 14px; color: #666; }
        .full-workflow { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 8px; padding: 20px; margin-bottom: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
        .full-workflow h2 { color: white; margin-bottom: 15px; font-size: 20px; text-align: center; }
        .workflow-controls { display: grid; grid-template-columns: 2fr 1fr; gap: 15px; align-items: end; }
        .workflow-left { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
        .workflow-control { }
        .workflow-control label { display: block; margin-bottom: 5px; color: white; font-weight: 600; font-size: 13px; }
        .workflow-control input, .workflow-control select { width: 100%; padding: 8px; border: 2px solid rgba(255,255,255,0.3); border-radius: 4px; font-size: 13px; background: rgba(255,255,255,0.9); }
        .workflow-button { height: 50px; }
        .btn-mega { background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%); font-size: 16px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); }
        .btn-mega:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(0,0,0,0.4); }
        .main-content { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 15px; }
        @media (max-width: 1400px) { .main-content { grid-template-columns: repeat(2, 1fr); } }
        @media (max-width: 900px) { .main-content { grid-template-columns: 1fr; } .workflow-controls { grid-template-columns: 1fr; } .workflow-left { grid-template-columns: 1fr; } }
        .panel { background: white; border-radius: 8px; padding: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .panel h2 { color: #333; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 2px solid #667eea; font-size: 16px; }
        .control-group { margin-bottom: 12px; }
        .control-group label { display: block; margin-bottom: 5px; color: #555; font-weight: 500; font-size: 13px; }
        .control-group input, .control-group select { width: 100%; padding: 8px; border: 2px solid #e5e7eb; border-radius: 4px; font-size: 13px; }
        .button-group { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 12px; }
        button { padding: 8px 12px; border: none; border-radius: 4px; font-size: 13px; font-weight: 600; cursor: pointer; transition: all 0.2s; color: white; }
        button:hover { transform: translateY(-1px); box-shadow: 0 2px 8px rgba(0,0,0,0.15); }
        button:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
        .btn-primary { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .btn-success { background: linear-gradient(135deg, #10b981 0%, #059669 100%); }
        .btn-info { background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); }
        .btn-warning { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); }
        .btn-danger { background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); }
        .btn-secondary { background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%); }
        .log-panel { grid-column: 1 / -1; }
        .log-container { background: #1e1e1e; border-radius: 6px; padding: 12px; height: 300px; overflow-y: auto; font-family: 'Courier New', monospace; font-size: 12px; }
        .log-entry { margin-bottom: 6px; padding: 4px; border-left: 2px solid transparent; }
        .log-entry.info { color: #3b82f6; border-left-color: #3b82f6; }
        .log-entry.success { color: #10b981; border-left-color: #10b981; }
        .log-entry.warning { color: #f59e0b; border-left-color: #f59e0b; }
        .log-entry.error { color: #ef4444; border-left-color: #ef4444; }
        .log-time { color: #9ca3af; margin-right: 8px; }
        .toast { position: fixed; top: 20px; right: 20px; padding: 12px 18px; border-radius: 6px; color: white; font-weight: 500; box-shadow: 0 4px 12px rgba(0,0,0,0.15); z-index: 1000; font-size: 14px; }
        .toast.success { background: #10b981; }
        .toast.error { background: #ef4444; }
        .toast.info { background: #3b82f6; }
        .hint { font-size: 11px; color: #666; margin-top: 4px; font-style: italic; }
        .workflow-hint { font-size: 11px; color: rgba(255,255,255,0.9); font-style: italic; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1> Social Media Hub 管理控制台</h1>
            <p>Instagram视频自动化处理与B站上传系统 - Docker容器化部署</p>
        </div>
        
        <div class="full-workflow">
            <h2> 一键执行完整流程</h2>
            <div class="workflow-controls">
                <div class="workflow-left">
                    <div class="workflow-control">
                        <label>账户</label>
                        <select id="workflow-account">
                            <option value="ai_vanvan">ai_vanvan</option>
                            <option value="aigf8728">aigf8728</option>
                        </select>
                    </div>
                    <div class="workflow-control">
                        <label>下载数量</label>
                        <input type="number" id="workflow-download" value="20" min="1" max="50">
                    </div>
                    <div class="workflow-control">
                        <label>合并数量</label>
                        <input type="number" id="workflow-merge" value="15" min="1" max="30">
                    </div>
                    <div class="workflow-control">
                        <label>分辨率</label>
                        <select id="workflow-resolution">
                            <option value="720x1280">720x1280 (竖屏HD)</option>
                            <option value="1080x1920">1080x1920 (竖屏FHD)</option>
                        </select>
                    </div>
                </div>
                <div class="workflow-button">
                    <button class="btn-mega" onclick="runFullWorkflow()" id="workflow-btn" style="width:100%;"> 执行全流程</button>
                    <div class="workflow-hint" style="margin-top:8px; text-align:center;">扫描下载标准化合并上传</div>
                </div>
            </div>
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
                    <button class="btn-primary" onclick="runAuth()"> 登录</button>
                    <button class="btn-secondary" onclick="checkAuthStatus()"> 状态</button>
                </div>
            </div>
            <div class="panel">
                <h2> 扫描新内容</h2>
                <div class="control-group">
                    <label>最大扫描数</label>
                    <input type="number" id="scan-limit" value="50" min="1" max="200">
                    <div class="hint"> 遇到已下载视频会自动停止</div>
                </div>
                <div class="button-group">
                    <button class="btn-success" onclick="runScanner()"> 扫描</button>
                    <button class="btn-secondary"> 结果</button>
                </div>
            </div>
            <div class="panel">
                <h2> 下载视频</h2>
                <div class="control-group">
                    <label>下载数量</label>
                    <input type="number" id="download-limit" value="20" min="1" max="50">
                    <div class="hint"> 默认20个，智能去重</div>
                </div>
                <div class="button-group">
                    <button class="btn-info" onclick="runDownloader()"> 下载</button>
                    <button class="btn-secondary"> 查看</button>
                </div>
            </div>
            <div class="panel">
                <h2> 标准化</h2>
                <div class="control-group">
                    <label>目标分辨率</label>
                    <select id="resolution">
                        <option value="720x1280">720x1280 (竖屏HD)</option>
                        <option value="1080x1920">1080x1920 (竖屏FHD)</option>
                    </select>
                </div>
                <div class="button-group">
                    <button class="btn-warning" onclick="runStandardizer()"> 处理</button>
                    <button class="btn-secondary"> 状态</button>
                </div>
            </div>
            <div class="panel">
                <h2> 合并视频</h2>
                <div class="control-group">
                    <label>合并数量</label>
                    <input type="number" id="merge-count" value="15" min="1" max="30">
                </div>
                <div class="button-group">
                    <button class="btn-primary" onclick="runMerger()"> 合并</button>
                    <button class="btn-secondary"> 查看</button>
                </div>
            </div>
            <div class="panel">
                <h2> B站上传</h2>
                <div class="control-group">
                    <label>视频文件</label>
                    <select id="video-select">
                        <option value="latest">最新合并视频</option>
                    </select>
                </div>
                <div class="button-group">
                    <button class="btn-danger" onclick="runUploader()"> 上传</button>
                    <button class="btn-secondary"> 历史</button>
                </div>
            </div>
            <div class="panel log-panel">
                <h2> 实时日志 <span style="float:right; font-size:12px; font-weight:normal; color:#666;">调试模式</span></h2>
                <div class="log-container" id="log-container">
                    <div class="log-entry info"><span class="log-time">[00:00:00]</span> 系统初始化完成，等待操作...</div>
                </div>
            </div>
        </div>
    </div>
    <script>
        let logCount = 0;
        const MAX_LOGS = 100;
        let isWorkflowRunning = false;
        
        function addLog(msg, type = 'info') {
            const log = document.getElementById('log-container');
            const time = new Date().toTimeString().split(' ')[0];
            const entry = document.createElement('div');
            entry.className = `log-entry ${type}`;
            entry.innerHTML = `<span class="log-time">[${time}]</span>${msg}`;
            log.appendChild(entry);
            log.scrollTop = log.scrollHeight;
            
            logCount++;
            if (logCount > MAX_LOGS) {
                log.removeChild(log.firstChild);
                logCount--;
            }
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
        
        async function runFullWorkflow() {
            if(isWorkflowRunning) {
                showToast('工作流正在执行中...', 'warning');
                return;
            }
            
            const account = document.getElementById('workflow-account').value;
            const downloadLimit = parseInt(document.getElementById('workflow-download').value);
            const mergeCount = parseInt(document.getElementById('workflow-merge').value);
            const resolution = document.getElementById('workflow-resolution').value;
            
            if(!confirm(` 确定执行完整流程？\n\n账户: ${account}\n下载: ${downloadLimit}个\n合并: ${mergeCount}个\n分辨率: ${resolution}\n\n流程: 扫描下载标准化合并上传`)) {
                return;
            }
            
            isWorkflowRunning = true;
            const btn = document.getElementById('workflow-btn');
            btn.disabled = true;
            btn.textContent = ' 执行中...';
            
            addLog('', 'info');
            addLog(' 开始执行完整流程', 'success');
            addLog(`账户: ${account} | 下载: ${downloadLimit} | 合并: ${mergeCount} | 分辨率: ${resolution}`, 'info');
            addLog('', 'info');
            
            try {
                // 步骤1: 扫描
                addLog('', 'info');
                addLog('【步骤1/5】 开始扫描新内容...', 'info');
                const scanResult = await callAPI('/api/scanner/scan', {account, limit: 50});
                if(scanResult.status === 'success') {
                    addLog(` 扫描任务已提交 (ID: ${scanResult.task_id})`, 'success');
                    await sleep(3000); // 等待3秒
                } else {
                    throw new Error('扫描失败: ' + scanResult.error);
                }
                
                // 步骤2: 下载
                addLog('', 'info');
                addLog(`【步骤2/5】 开始下载视频 (限制${downloadLimit}个)...`, 'info');
                const downloadResult = await callAPI('/api/downloader/download', {account, max_downloads: downloadLimit});
                if(downloadResult.status === 'success') {
                    addLog(` 下载任务已提交 (ID: ${downloadResult.task_id})`, 'success');
                    await sleep(5000); // 等待5秒
                } else {
                    throw new Error('下载失败: ' + downloadResult.error);
                }
                
                // 步骤3: 标准化
                addLog('', 'info');
                addLog(`【步骤3/5】 开始标准化处理 (${resolution})...`, 'info');
                const standardizeResult = await callAPI('/api/standardizer/process', {account, resolution});
                if(standardizeResult.status === 'success') {
                    addLog(` 标准化任务已提交 (ID: ${standardizeResult.task_id})`, 'success');
                    await sleep(5000); // 等待5秒
                } else {
                    throw new Error('标准化失败: ' + standardizeResult.error);
                }
                
                // 步骤4: 合并
                addLog('', 'info');
                addLog(`【步骤4/5】 开始合并视频 (${mergeCount}个)...`, 'info');
                const mergeResult = await callAPI('/api/merger/merge', {account, limit: mergeCount});
                if(mergeResult.status === 'success') {
                    addLog(` 合并任务已提交 (ID: ${mergeResult.task_id})`, 'success');
                    await sleep(5000); // 等待5秒
                } else {
                    throw new Error('合并失败: ' + mergeResult.error);
                }
                
                // 步骤5: 上传
                addLog('', 'info');
                addLog('【步骤5/5】 准备上传到B站...', 'info');
                const uploadResult = await callAPI('/api/uploader/upload', {account, video_path: null});
                if(uploadResult.status === 'success') {
                    addLog(` 上传任务已提交 (ID: ${uploadResult.task_id})`, 'success');
                } else {
                    throw new Error('上传失败: ' + uploadResult.error);
                }
                
                addLog('', 'info');
                addLog('', 'success');
                addLog(' 完整流程已全部提交！所有任务正在后台处理中...', 'success');
                addLog(' 提示: 可以通过docker logs命令查看各服务的详细执行情况', 'info');
                addLog('', 'success');
                
                showToast('完整流程已启动！', 'success');
                
            } catch(error) {
                addLog(` 流程执行失败: ${error.message}`, 'error');
                showToast('流程执行失败', 'error');
            } finally {
                isWorkflowRunning = false;
                btn.disabled = false;
                btn.textContent = ' 执行全流程';
            }
        }
        
        function sleep(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        }
        
        async function runAuth() {
            const account = document.getElementById('account-select').value;
            addLog(` 正在认证账户: ${account}...`, 'info');
            const result = await callAPI('/api/auth/login', {account});
            if(result.status === 'success') {
                addLog(` 账户认证成功: ${account}`, 'success');
                showToast('认证成功！', 'success');
            } else {
                addLog(` 认证失败: ${result.error}`, 'error');
                showToast('认证失败', 'error');
            }
        }
        
        async function checkAuthStatus() {
            const account = document.getElementById('account-select').value;
            addLog(` 检查账户状态: ${account}...`, 'info');
            const result = await fetch(`/api/auth/status/${account}`).then(r=>r.json());
            const status = result.authenticated ? ' 已认证' : ' 未认证';
            addLog(`状态: ${status}`, result.authenticated ? 'success' : 'warning');
        }
        
        async function runScanner() {
            const account = document.getElementById('account-select').value;
            const limit = document.getElementById('scan-limit').value;
            addLog(` 开始扫描 ${account}，最大 ${limit} 个帖子（遇到已下载自动停止）`, 'info');
            const result = await callAPI('/api/scanner/scan', {account, limit: parseInt(limit)});
            if(result.status === 'success') {
                addLog(` 扫描任务已提交到队列 (ID: ${result.task_id})`, 'success');
                showToast('扫描任务已创建！', 'success');
            } else {
                addLog(` 扫描失败: ${result.error}`, 'error');
                showToast('扫描失败', 'error');
            }
        }
        
        async function runDownloader() {
            const account = document.getElementById('account-select').value;
            const limit = document.getElementById('download-limit').value;
            addLog(` 开始下载视频，限制 ${limit} 个（智能去重）`, 'info');
            const result = await callAPI('/api/downloader/download', {account, max_downloads: parseInt(limit)});
            if(result.status === 'success') {
                addLog(` 下载任务已提交到队列 (ID: ${result.task_id})`, 'success');
                showToast('下载任务已创建！', 'success');
            } else {
                addLog(` 下载失败: ${result.error}`, 'error');
                showToast('下载失败', 'error');
            }
        }
        
        async function runStandardizer() {
            const account = document.getElementById('account-select').value;
            const resolution = document.getElementById('resolution').value;
            addLog(` 开始标准化处理，目标: ${resolution}`, 'info');
            const result = await callAPI('/api/standardizer/process', {account, resolution});
            if(result.status === 'success') {
                addLog(` 标准化任务已提交到队列 (ID: ${result.task_id})`, 'success');
                showToast('标准化任务已创建！', 'success');
            } else {
                addLog(` 标准化失败: ${result.error}`, 'error');
                showToast('标准化失败', 'error');
            }
        }
        
        async function runMerger() {
            const account = document.getElementById('account-select').value;
            const count = document.getElementById('merge-count').value;
            addLog(` 开始合并视频，数量: ${count}`, 'info');
            const result = await callAPI('/api/merger/merge', {account, limit: parseInt(count)});
            if(result.status === 'success') {
                addLog(` 合并任务已提交到队列 (ID: ${result.task_id})`, 'success');
                showToast('合并任务已创建！', 'success');
            } else {
                addLog(` 合并失败: ${result.error}`, 'error');
                showToast('合并失败', 'error');
            }
        }
        
        async function runUploader() {
            if(!confirm(' 确定要上传视频到B站吗？\n\n这将使用最新合并的视频文件。')) return;
            const account = document.getElementById('account-select').value;
            addLog(` 准备上传视频到B站...`, 'info');
            const result = await callAPI('/api/uploader/upload', {account, video_path: null});
            if(result.status === 'success') {
                addLog(` 上传任务已提交到队列 (ID: ${result.task_id})`, 'success');
                showToast('上传任务已创建！', 'success');
            } else {
                addLog(` 上传失败: ${result.error}`, 'error');
                showToast('上传失败', 'error');
            }
        }
        
        // 页面加载完成提示
        document.addEventListener('DOMContentLoaded', function() {
            addLog(' Web管理界面加载完成', 'success');
            addLog(' 提示: 扫描功能会在遇到已下载视频时自动停止，避免封号风险', 'info');
            addLog(' 新功能: 点击顶部"执行全流程"可一键完成所有步骤', 'info');
        });
    </script>
</body>
</html>
"@

$html | Out-File -FilePath "containers\api-gateway\templates\index.html" -Encoding UTF8
Write-Host " 添加全流程功能的HTML已创建"
