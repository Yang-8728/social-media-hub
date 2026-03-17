$body = @{
    account = "ai_vanvan"
    limit = 15
} | ConvertTo-Json

Write-Host "Sending request WITHOUT date (should use today: 2025-11-04):"
Write-Host $body

$response = Invoke-RestMethod -Uri "http://localhost:8080/api/merger/merge" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body

Write-Host "`nResponse:"
$response | ConvertTo-Json
