# Script will take user Emails from file 'users.csv' from directory, where script is located.
# It will return user IDs collected from Azure and save the result in 'users_uid'
# Note: users.csv should contain only Emails (No field names)

Connect-ExchangeOnline

$InputCsv  = "$PSScriptRoot\users.csv"
$OutputCsv = "$PSScriptRoot\users_uid.csv"

#Get-User -Identity username | Select-Object -ExpandProperty UserPrincipalName

$users = Get-Content -Path $InputCsv

foreach ($row in $users) {
    $user_email = $row
    try {
        $upn = Get-User -Identity $user_email | Select-Object -ExpandProperty UserPrincipalName
        $upn -replace "@lyreco\.com$", "" |  Out-File -FilePath $OutputCsv -Append
    } catch {
        "$user_email - ERROR: $_" | Out-File -FilePath $OutputCsv -Append
    }
}


Disconnect-ExchangeOnline