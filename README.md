# Wahoo Plan Converter

A Python library for converting YAML workout definitions to `.plan` format files, commonly used for structured cycling training workouts.

## Overview

This library allows you to define cycling workouts in a human-readable YAML format and convert them to the `.plan` format. The `.plan` format includes intervals with target power zones (as percentages of FTP), durations, and workout metadata.

## Wahoo Workout Generator CLI

This project also includes a CLI program to generate Wahoo .plan files and interval plots.

## Getting Started

### Windows Installation (Single Command)

1.  **Open PowerShell.** (You can search for "PowerShell" in the Windows Start Menu).
2.  **Paste and run the following command:**

    ```powershell
    irm https://raw.githubusercontent.com/sveinomork/wahoo_plane/main/setup.ps1 | iex
    ```

    *   This command will download the `setup.ps1` script directly from your GitHub repository and execute it.
    *   You might see a security warning from PowerShell about running scripts from the internet. You will need to confirm that you trust the source to proceed.

3.  **Follow the prompts:** The script will guide you through the installation process, checking for prerequisites like **Python**, Git and `uv` (Rye), cloning the repository, setting up the virtual environment, and installing the CLI.

4.  **Restart your terminal:** After the installation is complete, you might need to restart your PowerShell or Command Prompt window for the `wahoo` command to be recognized in your system's PATH.

### Manual Installation (Cross-Platform)

1.  **Open a terminal or command prompt.**
2.  **Navigate to the project directory:**
    ```
    cd C:\Users\som\coding\wahoo_plane
    ```
3.  **Activate the virtual environment:**
    *   On Windows:
        ```
        .venv\Scripts\activate
        ```
    *   On macOS and Linux:
        ```
        source .venv/bin/activate
        ```
4.  **Run the CLI:**
    ```
    wahoo
    ```
    This will start the workout generator and ask you if you want to generate a workout from a file or interactively.

### Installation

To install the dependencies, run the following command:

```
pip install -e .
```

## Testing

### Manual Testing

To manually test the CLI, run the `wahoo` command and choose the interactive mode. You can also create a YAML file and use the `from-file` mode.

### Automated Testing

To run the automated tests, run the following command:

```bash
# Run all tests
pytest
```

## YAML Workout Format

Define your workout in YAML format:

```yaml
name: 4x4 3-2-1
duration: 3420  # Total workout duration in seconds
tss: 62         # Training Stress Score
if: 0.81        # Intensity Factor
description:
  - 4x4 på 105%, avsluttet med 3-2-1 pyramide.
  - Selvkomponert
intervals:
  - name: WARM UP
    percent_ftp: 50
    duration: 300
  - name: Main Set
    repeat: 3
    subintervals:
      - name: 4 min Tempo
        percent_ftp: 105
        duration: 240
      - name: 3 min Recovery
        percent_ftp: 50
        duration: 180
  - name: Cool Down
    percent_ftp: 50
    duration: 600
```

## Development

### Project Structure

```
wahoo_plan/
├── src/
│   └── wahoo_plane/
│       ├── __init__.py
│       ├── cli.py
│       ├── interactive_workout.py
│       ├── plot_intervals.py
│       └── yaml_to_plan.py
├── tests/
│   ├── test_cli.py
│   └── test_yaml_to_plan.py
├── pyproject.toml
└── README.md
```

## Examples

See the included `4x4-3-2-1.plan` file for a complete example of the output format.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Run the test suite: `pytest`
5. Submit a pull request

## License

[Add your license here]
