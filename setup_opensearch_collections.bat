@echo off
setlocal enabledelayedexpansion

REM OpenSearch setup script for dental providers index
REM Based on instructions from setup_opensearch_collections.txt

REM Configuration
set OPENSEARCH_HOST=https://localhost:9200
set OPENSEARCH_USER=admin
set OPENSEARCH_PASS=V1b3#Coding
set INDEX_NAME=dental_providers
set DATA_FILE=provider_data.json

echo === OpenSearch Dental Providers Setup Script ===

REM 1. Check OpenSearch status
echo.
echo 1. Checking OpenSearch status...
curl -s -u "%OPENSEARCH_USER%:%OPENSEARCH_PASS%" "%OPENSEARCH_HOST%" --insecure >nul 2>&1
if %errorlevel% equ 0 (
    echo [SUCCESS] OpenSearch is running
) else (
    echo [ERROR] OpenSearch is not running or not accessible
    echo Please start OpenSearch and try again.
    exit /b 1
)

REM 2. Set variable for OpenSearch credentials
echo.
echo 2. Setting OpenSearch credentials...
set OPENSEARCH_AUTH=%OPENSEARCH_USER%:%OPENSEARCH_PASS%
    echo [SUCCESS] Credentials set: %OPENSEARCH_USER%:****

REM 3. Check if index exists, if not create it
echo.
echo 3. Checking if index '%INDEX_NAME%' exists...
for /f "tokens=*" %%i in ('curl -s -X GET "%OPENSEARCH_HOST%/%INDEX_NAME%" -u "%OPENSEARCH_AUTH%" --insecure') do set temp_check_index=%%i
echo [INFO] temp_check_index: %temp_check_index%
echo %temp_check_index% | findstr /C:"\"%INDEX_NAME%\"" >nul 2>&1
if %errorlevel% equ 0 (
    echo [SUCCESS] Index '%INDEX_NAME%' already exists
) else (
    echo Index '%INDEX_NAME%' does not exist. Creating...
    
    REM Create index with mapping
    curl -s -XPUT "%OPENSEARCH_HOST%/%INDEX_NAME%" -H "Content-Type: application/json" -u "%OPENSEARCH_AUTH%" --insecure -d"{\"settings\":{\"index\":{\"number_of_shards\":1,\"number_of_replicas\":1}},\"mappings\":{\"properties\":{\"name\":{\"type\":\"text\"},\"gender\":{\"type\":\"text\"},\"education\":{\"type\":\"text\"},\"reviews\":{\"type\":\"float\"},\"city\":{\"type\":\"text\"},\"state\":{\"type\":\"text\"},\"zip_code\":{\"type\":\"text\"},\"year_of_experience\":{\"type\":\"float\"},\"cost_efficiency\":{\"type\":\"float\"},\"specializations\":{\"type\":\"text\"},\"known_languages\":{\"type\":\"text\"}}},\"aliases\":{\"dental_care_providers\":{}}}" > temp_response.json
    
    findstr /c:"\"acknowledged\":true" temp_response.json >nul
    if %errorlevel% equ 0 (
        echo [SUCCESS] Index '%INDEX_NAME%' created successfully
    ) else (
        echo [ERROR] Failed to create index
        type temp_response.json
        del temp_response.json
        exit /b 1
    )
    del temp_response.json
)

REM 4. Read provider data and index it
echo.
echo 4. Reading provider data from %DATA_FILE% and indexing...

if not exist "%DATA_FILE%" (
    echo [ERROR] Data file '%DATA_FILE%' not found
    exit /b 1
)

echo Processing data without jq...

REM Create a simple bulk indexing format using PowerShell
powershell -File "process_data.ps1" "%DATA_FILE%" "%INDEX_NAME%"

if exist bulk_data.json (
    echo [SUCCESS] Bulk data prepared successfully
    
    REM Index the data using bulk API
    curl -s -XPOST "%OPENSEARCH_HOST%/_bulk" -H "Content-Type: application/x-ndjson" -u "%OPENSEARCH_AUTH%" --insecure --data-binary @bulk_data.json > temp_bulk_response.json
    
    REM Check for errors in bulk response (simple check)
    findstr /c:"\"errors\":false" temp_bulk_response.json >nul
    if %errorlevel% equ 0 (
        echo [SUCCESS] All documents indexed successfully
        REM Count documents from response
        findstr /c:"\"_index\":\"%INDEX_NAME%\"" temp_bulk_response.json | find /c /v "" > temp_count.txt
        set /p TOTAL_INDEXED=<temp_count.txt
        echo Total documents indexed: !TOTAL_INDEXED!
        del temp_count.txt
    ) else (
        echo [ERROR] Some documents failed to index
        echo Bulk response preview:
        type temp_bulk_response.json | findstr /c:"error" | findstr /c:"status"
    )
    
    REM Clean up temporary files
    del temp_bulk_response.json
    del bulk_data.json
) else (
    echo [ERROR] Failed to prepare bulk data
    exit /b 1
)

REM Final validation
echo.
echo Final validation...
curl -s -u "%OPENSEARCH_AUTH%" "%OPENSEARCH_HOST%/%INDEX_NAME%/_count" --insecure > temp_count.json
REM Extract count using PowerShell
powershell -Command "& { $response = Get-Content 'temp_count.json' | ConvertFrom-Json; Write-Host $response.count }" > temp_count_value.txt 2>nul
if exist temp_count_value.txt (
    set /p DOC_COUNT=<temp_count_value.txt
    del temp_count_value.txt
) else (
    set DOC_COUNT=unknown
)
echo [SUCCESS] Index '%INDEX_NAME%' is ready with %DOC_COUNT% documents
del temp_count.json

echo.
echo === Setup completed successfully! ===
echo Index name: %INDEX_NAME%
echo Alias: dental_care_providers
echo OpenSearch URL: %OPENSEARCH_HOST%

pause 