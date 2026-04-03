# Docker Setup & Testing Script for Surplusx
# Run from project root: powershell -ExecutionPolicy Bypass -File docker-setup.ps1

param(
    [string]$Action = "status",
    [switch]$Clean,
    [switch]$Rebuild
)

$projectRoot = "c:\Users\Saksham Rastogi\Downloads\Surplusx-1"
$composeFile = "docker-compose.dev.yml"

function Write-Header {
    param([string]$Text)
    Write-Host "`n" -NoNewline
    Write-Host "=" * 70 -ForegroundColor Cyan
    Write-Host $Text -ForegroundColor Cyan
    Write-Host "=" * 70 -ForegroundColor Cyan
}

function Write-Status {
    param([string]$Text, [string]$Type = "info")
    switch($Type) {
        "success" { Write-Host "✅ $Text" -ForegroundColor Green }
        "error"   { Write-Host "❌ $Text" -ForegroundColor Red }
        "warning" { Write-Host "⚠️  $Text" -ForegroundColor Yellow }
        default   { Write-Host "ℹ️  $Text" -ForegroundColor Cyan }
    }
}

function Cleanup {
    Write-Header "Cleaning Up Docker Resources"
    
    Write-Status "Stopping all containers..."
    docker-compose -f $composeFile down
    
    Write-Status "Removing volumes for clean database..."
    docker-compose -f $composeFile down -v
    
    Write-Status "Cleanup complete" "success"
}

function BuildImages {
    Write-Header "Building Docker Images"
    
    Write-Status "Building images (this may take a few minutes)..."
    docker-compose -f $composeFile build
    
    if ($LASTEXITCODE -eq 0) {
        Write-Status "Images built successfully" "success"
    } else {
        Write-Status "Build failed" "error"
        exit 1
    }
}

function StartServices {
    Write-Header "Starting Services"
    
    Write-Status "Starting Docker services..."
    Write-Status "Frontend will be available at: http://localhost:3000"
    Write-Status "Backend will be available at: http://localhost:5000"
    Write-Status "MySQL will be available at: localhost:3306"
    Write-Status "Press Ctrl+C to stop services`n"
    
    docker-compose -f $composeFile up
}

function CheckStatus {
    Write-Header "Checking Service Status"
    
    Write-Status "Running containers:"
    docker-compose -f $composeFile ps
    
    Write-Host "`n"
    Write-Status "Recent service logs:"
    docker-compose -f $composeFile logs --tail=20
}

function TestConnections {
    Write-Header "Testing Service Connections"
    
    # Check if containers are running
    $containers = docker-compose -f $composeFile ps --services --filter "status=running"
    
    Write-Status "Running containers: $($containers -join ', ')"
    
    # Test MySQL
    Write-Status "Testing MySQL connection..."
    try {
        $result = docker exec surplusx-1-db-1 mysqladmin ping -h localhost -u root -prootpassword 2>&1
        if ($result -like "*mysqld is alive*") {
            Write-Status "MySQL is responding" "success"
        } else {
            Write-Status "MySQL health check returned: $result"
        }
    } catch {
        Write-Status "Could not connect to MySQL: $_" "warning"
    }
    
    # Test Backend connectivity (simple check)
    Write-Status "Testing Backend..."
    try {
        $backendLogs = docker-compose -f $composeFile logs backend 2>&1
        if ($backendLogs -like "*running on*" -or $backendLogs -like "*Database tables initialized*") {
            Write-Status "Backend is running" "success"
        } else {
            Write-Status "Backend status: check logs" "warning"
            Write-Host $backendLogs
        }
    } catch {
        Write-Status "Could not check backend: $_" "warning"
    }
    
    # Test Frontend
    Write-Status "Testing Frontend..."
    try {
        $frontendLogs = docker-compose -f $composeFile logs frontend 2>&1
        if ($frontendLogs -like "*ready*" -or $frontendLogs -like "*vite*") {
            Write-Status "Frontend is running on http://localhost:3000" "success"
        } else {
            Write-Status "Frontend status: check logs" "warning"
        }
    } catch {
        Write-Status "Could not check frontend: $_" "warning"
    }
}

function ShowLogs {
    param([string]$Service = "all")
    
    Write-Header "Displaying Logs (Last 50 lines)"
    
    if ($Service -eq "all") {
        docker-compose -f $composeFile logs --tail=50
    } else {
        Write-Status "Showing logs for: $Service"
        docker-compose -f $composeFile logs --tail=50 $Service
    }
}

function RestartService {
    param([string]$Service = "all")
    
    Write-Header "Restarting Service(s)"
    
    if ($Service -eq "all") {
        Write-Status "Restarting all services..."
        docker-compose -f $composeFile restart
    } else {
        Write-Status "Restarting $Service..."
        docker-compose -f $composeFile restart $Service
    }
    
    Write-Status "Services restarted" "success"
}

# Main execution
Set-Location $projectRoot

Write-Host "`n"
Write-Host "╔════════════════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
Write-Host "║           🐳 Surplusx Docker Setup & Testing Tool 🐳             ║" -ForegroundColor Magenta
Write-Host "╚════════════════════════════════════════════════════════════════════╝" -ForegroundColor Magenta

switch($Action.ToLower()) {
    "start" {
        if ($Clean) { Cleanup }
        if ($Rebuild -or $Clean) { BuildImages }
        StartServices
    }
    
    "clean" {
        Cleanup
        if ($Rebuild) { BuildImages }
    }
    
    "rebuild" {
        Cleanup
        BuildImages
        StartServices
    }
    
    "status" {
        CheckStatus
        TestConnections
    }
    
    "logs" {
        if ($Rebuild) {
            ShowLogs $Rebuild
        } else {
            ShowLogs
        }
    }
    
    "restart" {
        if ($Rebuild) {
            RestartService $Rebuild
        } else {
            RestartService
        }
    }
    
    "test" {
        TestConnections
    }
    
    default {
        Write-Host @"
Usage: powershell -ExecutionPolicy Bypass -File docker-setup.ps1 [Action] [Options]

Actions:
  start       - Start Docker services (default)
  clean       - Stop and clean up all containers/volumes
  rebuild     - Clean build and start (full reset)
  status      - Show status and test connections
  logs        - Show service logs
  restart     - Restart services
  test        - Test all connections

Options:
  -Clean      - Clean up before starting
  -Rebuild    - Rebuild images before starting

Examples:
  # Start services normally
  .\docker-setup.ps1 start

  # Clean reset and start
  .\docker-setup.ps1 start -Clean -Rebuild

  # Show logs for backend only
  .\docker-setup.ps1 logs -Rebuild backend

  # Check current status
  .\docker-setup.ps1 status

"@ -ForegroundColor Yellow
    }
}

Write-Host "`n"
