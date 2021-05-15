cd c://TESTS/path
set HOME=%USERPROFILE%
cd "C:\Automation\AutoEHR"
git checkout -- "*.ipynb"
git pull origin main
jupyter lab
