# Wahoo Plan Converter

A Python library for converting YAML workout definitions to `.plan` format files, commonly used for structured cycling training workouts.

## Overview

This library allows you to define cycling workouts in a human-readable YAML format and convert them to the `.plan` format. The `.plan` format includes intervals with target power zones (as percentages of FTP), durations, and workout metadata.

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd wahoo_plan

# Install dependencies using uv
uv sync

# Or install manually
uv pip install pyyaml pytest
```

## Usage

### YAML Workout Format

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

### Converting YAML to .plan

#### As a Python Module

```python
from yaml_to_plan import yaml_to_plan
import yaml

# Load YAML workout
with open('workout.yaml', 'r') as f:
    workout_data = yaml.safe_load(f)

# Convert to .plan format
plan_content = yaml_to_plan(workout_data)

# Save to file
with open('workout.plan', 'w') as f:
    f.write(plan_content)
```

#### Command Line

```bash
python yaml_to_plan.py input.yaml output.plan
```

## YAML Schema

### Required Fields
- `name`: Workout name (string)
- `duration`: Total duration in seconds (integer)
- `tss`: Training Stress Score (integer)
- `if`: Intensity Factor (float)
- `intervals`: List of workout intervals

### Interval Structure
```yaml
intervals:
  - name: "Interval Name"           # Required
    percent_ftp: 105               # Required: Target power as % of FTP
    duration: 240                  # Required: Duration in seconds
    repeat: 3                      # Optional: Number of repetitions
    subintervals:                  # Optional: For complex interval blocks
      - name: "Sub-interval"
        percent_ftp: 105
        duration: 240
```

## Generated .plan Format

The converter generates files compatible with training software that uses the `.plan` format:

```
=HEADER=

NAME=4x4 3-2-1
DURATION=3420

TSS=62
IF=0.81

DESCRIPTION=4x4 på 105%, avsluttet med 3-2-1 pyramide.

=STREAM=

=INTERVAL=
INTERVAL_NAME=WARM UP
PERCENT_FTP_HI=50
MESG_DURATION_SEC>=300?EXIT
```

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_yaml_to_plan.py
```

### Project Structure

```
wahoo_plan/
├── yaml_to_plan.py          # Main converter module
├── tests/
│   └── test_yaml_to_plan.py # Test suite
├── pyproject.toml           # Project configuration
└── README.md               # This file
```

## Examples

See the included `4x4-3-2-1.plan` file for a complete example of the output format.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Run the test suite: `uv run pytest`
5. Submit a pull request

## License

[Add your license here]