
param(
    [string]$InterfaceName = "WireGuard Tunnel",
    [string]$Dns = "10.8.0.1"
)

Write-Host "Applying kill switch for interface: $InterfaceName"

# Find the interface index
$ifIndex = (Get-NetIPInterface | Where-Object {$_.InterfaceAlias -eq $InterfaceName}).InterfaceIndex
if (-not $ifIndex) {
    Write-Error "Interface '$InterfaceName' not found. Make sure the tunnel is active."
    exit 1
}

# 1) Block all outbound except via WireGuard interface
New-NetFirewallRule -DisplayName "CustomVPN KillSwitch OUT" -Direction Outbound -Action Block -Enabled True -Profile Any -InterfaceAlias "*"
New-NetFirewallRule -DisplayName "CustomVPN Allow WG OUT" -Direction Outbound -Action Allow -Enabled True -Profile Any -InterfaceAlias $InterfaceName

# 2) Force DNS to VPN resolver
$adapters = Get-DnsClientServerAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -eq $InterfaceName}
if (-not $adapters) {
    Set-DnsClientServerAddress -InterfaceAlias $InterfaceName -ServerAddresses $Dns
} else {
    Set-DnsClientServerAddress -InterfaceAlias $InterfaceName -ServerAddresses $Dns
}

Write-Host "Kill switch and DNS pinned to $Dns applied."
Write-Host "Optional: add split-tunnel routes by editing client\\routing-rules.json and applying them here."
