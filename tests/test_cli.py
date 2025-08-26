
import os
import yaml
from click.testing import CliRunner
from wahoo_plane.cli import cli

def test_cli_no_args():
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code != 0
    assert 'Usage: cli [OPTIONS] COMMAND [ARGS]' in result.output

def test_from_file_command(tmp_path):
    runner = CliRunner()
    yaml_file = tmp_path / "test.yaml"
    yaml_content = {
        "name": "Test Workout",
        "duration": 1800,
        "tss": 30,
        "if": 0.6,
        "intervals": [
            {"name": "Endurance", "percent_ftp": 70, "duration": 1800}
        ]
    }
    with open(yaml_file, 'w') as f:
        yaml.dump(yaml_content, f)

    result = runner.invoke(cli, ["from-file", str(yaml_file)])
    assert result.exit_code == 0

    plan_file = tmp_path / "test.plan"
    png_file = tmp_path / "test.png"

    assert os.path.exists(plan_file)
    assert os.path.exists(png_file)

    with open(plan_file, 'r') as f:
        plan_content = f.read()
        assert "NAME=Test Workout" in plan_content
        assert "INTERVAL_NAME=Endurance" in plan_content
