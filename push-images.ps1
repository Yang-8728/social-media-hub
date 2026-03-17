# Push all images to Huawei SWR

$env:DOCKER_BUILDKIT = 0
$SWR = "swr.ap-southeast-2.myhuaweicloud.com/smh"

$images = @("auth", "scanner", "downloader", "standardizer", "merger", "uploader", "biliup-uploader")

Write-Host "Start pushing images to SWR..." -ForegroundColor Green

foreach ($image in $images) {
    $remoteImage = "$SWR/${image}:latest"
    
    Write-Host "`n[$image] Building..." -ForegroundColor Cyan
    
    Push-Location "containers/$image"
    docker build -t $remoteImage .
    Pop-Location
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[$image] Build failed" -ForegroundColor Red
        continue
    }
    
    Write-Host "[$image] Pushing..." -ForegroundColor Cyan
    docker push $remoteImage
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[$image] Success" -ForegroundColor Green
    } else {
        Write-Host "[$image] Failed" -ForegroundColor Red
    }
}

Write-Host "`nAll done!" -ForegroundColor Green
