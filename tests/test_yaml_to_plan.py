import yaml
from wahoo_plane.yaml_to_plan import yaml_to_plan

def test_yaml_to_plan_basic():
    yaml_input = {
        "name": "4x4 3-2-1",
        "duration": 3420,
        "tss": 62,
        "if": 0.81,
        "description": [
            "4x4 på 105%, avsluttet med 3-2-1 pyramide.",
            "Selvkomponert"
        ],
        "intervals": [
            {"name": "WARM UP", "percent_ftp": 50, "duration": 300},
            {"name": "WARM UP 2", "percent_ftp": 60, "duration": 300},
            {
                "name": "4X2min 75-65",
                "repeat": 3,
                "subintervals": [
                    {"name": "4 min Tempo", "percent_ftp": 105, "duration": 240},
                    {"name": "3 min Hvile", "percent_ftp": 50, "duration": 180}
                ]
            },
            {"name": "3 min", "percent_ftp": 105, "duration": 180},
            {"name": "2 min Hvile", "percent_ftp": 50, "duration": 120},
            {"name": "2 min", "percent_ftp": 105, "duration": 120},
            {"name": "1 min Hvile", "percent_ftp": 50, "duration": 60},
            {"name": "1 min", "percent_ftp": 105, "duration": 60},
            {"name": "Recovery", "percent_ftp": 50, "duration": 600}
        ]
    }

    plan_output = yaml_to_plan(yaml_input)
    assert "NAME=4x4 3-2-1" in plan_output
    assert "DURATION=3420" in plan_output
    assert "INTERVAL_NAME=WARM UP" in plan_output
    assert "REPEAT=3" in plan_output
    assert "INTERVAL_NAME=4 min Tempo" in plan_output
    assert "MESG_DURATION_SEC>=600?EXIT" in plan_output