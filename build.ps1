$exclude = @("venv", "automacao_youtube.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "automacao_youtube.zip" -Force