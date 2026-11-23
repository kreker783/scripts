param(
    [Parameter(Mandatory=$true)]
    [string]$username
)

Get-ADUser $username -Properties MemberOf |
    Select-Object -ExpandProperty MemberOf |
    ForEach-Object { ($_ -split ",")[0] -replace "^CN=" } |
    Sort-Object