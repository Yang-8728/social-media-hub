$body = @{
    account = "ai_vanvan"
    date = "2025-11-03"
    limit = 15
} | ConvertTo-Json

Write-Host "Sending request with body:"
Write-Host $body

$response = Invoke-RestMethod -Uri "http://localhost:8080/api/merger/merge" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body

Write-Host "`nResponse:"
$response | ConvertTo-Json
