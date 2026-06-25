param(
    [Parameter(Mandatory = $true)]
    [string]$Message,

    [int]$Top = 3,

    [switch]$Log,

    [string]$Root = $null
)

$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($Root)) {
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    $Root = (Resolve-Path (Join-Path $scriptDir '..')).Path
}

$routePath = Join-Path $Root 'skill-routing-table.json'
if (-not (Test-Path -LiteralPath $routePath)) {
    throw "Route table not found: $routePath"
}

$table = Get-Content -LiteralPath $routePath -Encoding UTF8 -Raw | ConvertFrom-Json

function Resolve-SkillPath {
    param([string]$Skill)

    $candidates = @(
        (Join-Path $Root "skills\$Skill"),
        (Join-Path $env:USERPROFILE ".codex\skills\$Skill"),
        (Join-Path $env:USERPROFILE ".newmax\skills\$Skill")
    )

    foreach ($candidate in $candidates) {
        if (Test-Path -LiteralPath (Join-Path $candidate 'SKILL.md')) {
            return $candidate
        }
    }

    return $null
}

function Get-TriggerHits {
    param(
        [string]$Text,
        [object[]]$Triggers
    )

    $hits = New-Object System.Collections.Generic.List[string]
    foreach ($trigger in $Triggers) {
        $t = [string]$trigger
        if ([string]::IsNullOrWhiteSpace($t)) {
            continue
        }

        if ($Text.IndexOf($t, [StringComparison]::OrdinalIgnoreCase) -ge 0) {
            $hits.Add($t)
        }
    }

    return $hits.ToArray()
}

$matches = foreach ($route in $table.routes) {
    if ($route.auto -ne $true) {
        continue
    }

    $hits = Get-TriggerHits -Text $Message -Triggers $route.triggers
    if ($hits.Count -eq 0) {
        continue
    }

    $priority = [int]$route.priority
    $confidence = [double]$route.confidence
    $score = ($hits.Count * 10) + ($confidence * 5) + [Math]::Max(0, 10 - $priority)
    $skillPath = Resolve-SkillPath -Skill $route.skill

    [PSCustomObject]@{
        id = $route.id
        name = $route.name
        skill = $route.skill
        skillPath = $skillPath
        mcp = $route.mcp
        priority = $priority
        confidence = $confidence
        score = [Math]::Round($score, 2)
        triggerHits = $hits
        note = $route.note
    }
}

$ranked = @($matches | Sort-Object -Property @{ Expression = 'score'; Descending = $true }, @{ Expression = 'priority'; Ascending = $true } | Select-Object -First $Top)

$result = [PSCustomObject]@{
    matched = ($ranked.Count -gt 0)
    message = $Message
    selected = if ($ranked.Count -gt 0) { $ranked[0] } else { $null }
    candidates = $ranked
}

if ($Log -and $ranked.Count -gt 0) {
    $logPath = Join-Path $Root 'memory\skill-usage-log.md'
    $now = Get-Date -Format 'yyyy-MM-dd HH:mm'
    $selected = $ranked[0]
    $line = @"

### $now #auto-route
- **触发**：$Message
- **路由**：$($selected.id) → $($selected.skill)
- **命中词**：$($selected.triggerHits -join ', ')
- **结果**：待执行
- **反馈**：无
- **调整**：无
"@
    Add-Content -LiteralPath $logPath -Encoding UTF8 -Value $line
}

$result | ConvertTo-Json -Depth 8
