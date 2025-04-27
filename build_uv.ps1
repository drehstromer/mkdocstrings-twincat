# Build and publish the mkdocstrings-twincat package using uv

# Clean up previous builds
if (Test-Path -Path "dist") {
    Write-Host "Cleaning up previous builds..."
    Remove-Item -Path "dist" -Recurse -Force
}

# Build the package
Write-Host "Building package with uv..."
uv build
Write-Host "Package built successfully."

# Ask if the user wants to publish the package
$publish = Read-Host -Prompt "Do you want to publish the package to PyPI? (y/n)"
if ($publish -eq "y") {
    Write-Host "Publishing package to PyPI with uv..."
    uv publish dist/*
    Write-Host "Package published successfully."
}
else {
    Write-Host "Package not published."
}

Write-Host "Done."
