from cx_Freeze import setup, Executable
base = None
executables = [Executable("risk.py", base=base)]
packages = ["random", "pygame"]
options = {
    'build_exe': {    
        'packages':packages,
    },
}
setup(
    name = "risk",
    options = options,
    version = "1.0",
    description = 'jeu de plateau',
    executables = executables
)
