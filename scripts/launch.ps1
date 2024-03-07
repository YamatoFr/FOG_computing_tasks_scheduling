$reportFolder = "C:\Users\theof\OneDrive\Documents\Github\FOG_computing_tasks_scheduling\report"  # Replace with the actual path to your report folder

# Get all the .tex files in the report folder
$texFiles = Get-ChildItem -Path $reportFolder -Filter "*.tex" -File

# Loop through each .tex file and launch citationcheck.py
# with the first argument being the name of the .tex file (except for rapport_para.tex, which is the main report file)
# and the second argument being the mode of operation (1, 2 or 3. See citationcheck.py for details)

# Input mode in console
$mode = Read-Host "Enter the mode of operation (1, 2 or 3)"

foreach ($texFile in $texFiles) {
	if ($texFile.Name -ne "rapport_para.tex") {
		$fileName = $texFile.Name.Replace(".tex", "")
		python .\scripts\citationcheck.py $fileName $mode
		# print the name of the file to the console
		Write-Host $fileName
	}
}
