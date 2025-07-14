import subprocess
import os

def run_savilerow_and_minion(eprime_file: str, param_file: str):
    base_dir = os.path.dirname(os.path.abspath(__file__))

    jar_path = os.path.join(base_dir, 'SavileRow.jar')
    eprime_path = os.path.join(base_dir, eprime_file)
    param_path = os.path.join(base_dir, param_file)
    minion_exe = os.path.join(base_dir, 'bin', 'minion.exe')
    minion_file = param_path + '.minion'

    # Run Savile Row without auto-running Minion
    command = [
    'java', '-jar', jar_path, eprime_path, param_path,
    '-minion-bin', r'c:\Users\pavle\Desktop\acmg_2\savilerow-1.6.5-windows\bin\minion.exe'
    ]
    print("Running Savile Row:\n", " ".join(command))
    result = subprocess.run(command, capture_output=True, text=True, cwd=base_dir)
    print("Savile Row output:\n", result.stdout)
    print("Savile Row errors:\n", result.stderr)

    if not os.path.exists(minion_file):
        print(f"Minion input file not found: {minion_file}")
        return

    if not os.path.exists(minion_exe):
        print(f"Minion executable not found: {minion_exe}")
        return

    # Run Minion manually
    print(f"Running Minion on {minion_file}")
    minion_result = subprocess.run([minion_exe, minion_file], capture_output=True, text=True)
    print("Minion output:\n", minion_result.stdout)
    if minion_result.stderr:
        print("Minion errors:\n", minion_result.stderr)

if __name__ == '__main__':
    run_savilerow_and_minion('sudoku.eprime', 'sudoku.param')
