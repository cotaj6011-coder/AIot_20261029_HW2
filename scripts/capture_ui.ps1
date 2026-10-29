param(
    [string]$WebSocketUrl,
    [string]$DesktopPath,
    [string]$MobilePath,
    [string]$AnalysisPath = ''
)

$socket = [System.Net.WebSockets.ClientWebSocket]::new()
$socket.ConnectAsync([Uri]$WebSocketUrl, [Threading.CancellationToken]::None).GetAwaiter().GetResult()
$script:messageId = 0

function Invoke-Cdp {
    param([string]$Method, [hashtable]$Params = @{})
    $script:messageId++
    $id = $script:messageId
    $json = @{id = $id; method = $Method; params = $Params} | ConvertTo-Json -Compress -Depth 20
    $bytes = [Text.Encoding]::UTF8.GetBytes($json)
    $segment = [ArraySegment[byte]]::new($bytes)
    $socket.SendAsync($segment, [Net.WebSockets.WebSocketMessageType]::Text, $true,
        [Threading.CancellationToken]::None).GetAwaiter().GetResult()
    while ($true) {
        $stream = [IO.MemoryStream]::new()
        do {
            $buffer = New-Object byte[] 65536
            $result = $socket.ReceiveAsync([ArraySegment[byte]]::new($buffer),
                [Threading.CancellationToken]::None).GetAwaiter().GetResult()
            $stream.Write($buffer, 0, $result.Count)
        } while (-not $result.EndOfMessage)
        $message = [Text.Encoding]::UTF8.GetString($stream.ToArray()) | ConvertFrom-Json
        if ($message.id -eq $id) { return $message }
    }
}

Invoke-Cdp -Method 'Runtime.enable' | Out-Null
$deadline = [DateTime]::UtcNow.AddSeconds(20)
do {
    Start-Sleep -Milliseconds 400
    $state = Invoke-Cdp -Method 'Runtime.evaluate' -Params @{
        expression = "JSON.stringify({title:document.title,hero:document.querySelector('.hero')?.innerText||'',tabs:[...document.querySelectorAll('[role=tab]')].map(x=>x.innerText),buttons:[...document.querySelectorAll('[data-testid=stSidebar] button')].map(x=>({text:x.innerText,testid:x.dataset.testid,aria:x.getAttribute('aria-label')})),body:document.body.innerText.slice(0,800)})"
        returnByValue = $true
    }
    $evidence = $state.result.result.value | ConvertFrom-Json
} while ([string]::IsNullOrWhiteSpace($evidence.hero) -and [DateTime]::UtcNow -lt $deadline)

if ([string]::IsNullOrWhiteSpace($evidence.hero)) { throw 'Streamlit hero did not finish rendering.' }
$evidence | ConvertTo-Json -Depth 5

Invoke-Cdp -Method 'Emulation.setDeviceMetricsOverride' -Params @{width=1440;height=1100;deviceScaleFactor=1;mobile=$false} | Out-Null
Invoke-Cdp -Method 'Page.reload' | Out-Null
Start-Sleep -Seconds 2
$desktop = Invoke-Cdp -Method 'Page.captureScreenshot' -Params @{format='png';captureBeyondViewport=$false}
[IO.File]::WriteAllBytes($DesktopPath, [Convert]::FromBase64String($desktop.result.data))

if (-not [string]::IsNullOrWhiteSpace($AnalysisPath)) {
    $buttonBounds = Invoke-Cdp -Method 'Runtime.evaluate' -Params @{
        expression = "(()=>{const b=document.querySelector('[data-testid=stSidebar] [data-testid=stBaseButton-primary]');if(!b)return '';const r=b.getBoundingClientRect();return JSON.stringify({x:r.x+r.width/2,y:r.y+r.height/2})})()"
        returnByValue = $true
    }
    if ([string]::IsNullOrWhiteSpace($buttonBounds.result.result.value)) { throw 'Analyze button was not found.' }
    $point = $buttonBounds.result.result.value | ConvertFrom-Json
    Invoke-Cdp -Method 'Input.dispatchMouseEvent' -Params @{type='mousePressed';x=$point.x;y=$point.y;button='left';clickCount=1} | Out-Null
    Invoke-Cdp -Method 'Input.dispatchMouseEvent' -Params @{type='mouseReleased';x=$point.x;y=$point.y;button='left';clickCount=1} | Out-Null
    $analysisDeadline = [DateTime]::UtcNow.AddSeconds(45)
    do {
        Start-Sleep -Milliseconds 500
        $analysisState = Invoke-Cdp -Method 'Runtime.evaluate' -Params @{
            expression = "document.body.innerText.includes('Baseline vs Selected')"
            returnByValue = $true
        }
        $analysisReady = $analysisState.result.result.value
    } while (-not $analysisReady -and [DateTime]::UtcNow -lt $analysisDeadline)
    if (-not $analysisReady) { throw 'Full analysis did not finish rendering.' }
    Invoke-Cdp -Method 'Runtime.evaluate' -Params @{
        expression = "[...document.querySelectorAll('[role=tab]')].find(x=>x.innerText.includes('05 評估診斷'))?.click()"
        returnByValue = $true
    } | Out-Null
    Start-Sleep -Milliseconds 800
    $analysisShot = Invoke-Cdp -Method 'Page.captureScreenshot' -Params @{format='png';captureBeyondViewport=$false}
    [IO.File]::WriteAllBytes($AnalysisPath, [Convert]::FromBase64String($analysisShot.result.data))
}

Invoke-Cdp -Method 'Emulation.setDeviceMetricsOverride' -Params @{width=430;height=932;deviceScaleFactor=1;mobile=$true} | Out-Null
Start-Sleep -Milliseconds 500
$mobile = Invoke-Cdp -Method 'Page.captureScreenshot' -Params @{format='png';captureBeyondViewport=$false}
[IO.File]::WriteAllBytes($MobilePath, [Convert]::FromBase64String($mobile.result.data))

$socket.CloseAsync([Net.WebSockets.WebSocketCloseStatus]::NormalClosure, 'done',
    [Threading.CancellationToken]::None).GetAwaiter().GetResult()
