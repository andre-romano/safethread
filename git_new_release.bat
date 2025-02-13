@echo off
call .\activate.bat

echo 1) Installing bump2version ...
pip install bump2version

echo 2) Creating a new version ...
bump2version patch  # ou minor/major

echo 3) Commiting ...
call .\git_add_commit.bat 'release new version'

echo 4) Tagging ...
for /f %%v in ('.\get_version.bat') do call .\git_tag.bat %%v



