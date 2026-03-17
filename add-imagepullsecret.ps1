# 给所有 Deployment YAML 添加 imagePullSecrets
$services = @("redis", "scanner", "downloader", "standardizer", "merger", "uploader", "auth", "biliup-uploader")

foreach ($service in $services) {
    $file = "k8s\cce\$service.yaml"
    if (Test-Path $file) {
        $content = Get-Content $file -Raw
        $newContent = $content -replace '(\s+spec:\s+\n\s+containers:)', "`$1`n      imagePullSecrets:`n      - name: swr-secret`n     "
        $newContent | Set-Content $file
        Write-Host "Updated $service.yaml"
    }
}
