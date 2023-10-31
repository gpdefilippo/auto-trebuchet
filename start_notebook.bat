@echo off

set envName=auto_trebuchet
set pythonVersion=3.12.0
set requirementsFile=requirements.txt
set notebookFile=run_design.ipynb

REM Check if the environment exists
conda activate %envName%
if %errorlevel%==1 (
    echo Environment "%envName%" does not exist. Creating...
    conda create -n %envName% python=%pythonVersion%
    conda activate %envName%
    conda install -n %envName% --file %requirementsFile%
) else (
    echo Environment "%envName%" already exists. Activating...
    conda activate %envName%
)

REM Start Jupyter Notebook
jupyter notebook %notebookFile%