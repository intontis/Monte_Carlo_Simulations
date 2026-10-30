
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent

NOTEBOOKS = {
    "pi": PROJECT_ROOT / "notebooks" / "01_pi_estimation.ipynb",
    "scattering": PROJECT_ROOT / "notebooks" / "02_particle_scattering.ipynb",
}


def run_notebook(name, timeout):
    # Execute one notebook and generate its results
    notebook = NOTEBOOKS[name]

    if not notebook.is_file():
        raise FileNotFoundError(f"Notebook not found: {notebook}")

    print(f"\nRunning simulation: {name}")
    print(f"Notebook: {notebook.name}")

    with tempfile.TemporaryDirectory(prefix="monte-carlo-") as output_dir:
        command = [
            sys.executable,
            "-m",
            "nbconvert",
            "--to",
            "notebook",
            "--execute",
            f"--ExecutePreprocessor.timeout={timeout}",
            "--output-dir",
            output_dir,
            "--output",
            f"{notebook.stem}_executed.ipynb",
            str(notebook),
        ]

        subprocess.run(command, cwd=PROJECT_ROOT, check=True)

    print(f"\n{name.capitalize()} simulation completed successfully.")


def main():
    parser = argparse.ArgumentParser(
        description="Run Monte Carlo simulations from the project notebooks."
    )

    parser.add_argument(
        "simulation",
        choices=["pi", "scattering", "all"],
        help="Select which simulation to execute.",
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=600,
        help="Maximum execution time per notebook in seconds (default: 600).",
    )

    args = parser.parse_args()

    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero")

    selected = (
        list(NOTEBOOKS)
        if args.simulation == "all"
        else [args.simulation]
    )

    try:
        for name in selected:
            run_notebook(name, args.timeout)
    except (FileNotFoundError, subprocess.CalledProcessError) as error:
        print(f"\nSimulation failed: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
