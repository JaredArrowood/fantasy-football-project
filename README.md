# fantasy-football-project

## Prerequisites

1. create the virtual encvironment

   > python3 -m venv venv

2. activate the venv

   > .\venv\Scripts\activate.ps1 (for powershell)

   > .\venv\Scripts\activate.bat (for cmdline)

   > .\venv\Scripts\activate (if neither work)

(if your system says you can't run scripts, run:

> Get-ExecutionPolicy -Scope CurrentUser

if it is restricted or undefined, run:

> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser)

3. install requirements
   > pip install -r requirements.txt

## Orders of bizness

1. Create CLI
2. Create a DB
3. Put it all together
