import yaml
import os

def yaml_to_plan(yaml_data):
    lines = []
    lines.append("=HEADER=")
    lines.append("")
    lines.append(f"NAME={yaml_data['name']}")
    lines.append(f"DURATION={yaml_data['duration']}")
    lines.append("")
    lines.append(f"TSS={yaml_data['tss']}")
    lines.append(f"IF={yaml_data['if']}")
    lines.append("")
    for desc in yaml_data.get('description', []):
        lines.append(f"DESCRIPTION={desc}")
    lines.append("")
    lines.append("=STREAM=")
    lines.append("")

    for interval in yaml_data['intervals']:
        if 'subintervals' in interval:
            lines.append("=INTERVAL=")
            lines.append(f"INTERVAL_NAME={interval['name']}")
            if 'repeat' in interval:
                lines.append(f"REPEAT={interval['repeat']}")
            lines.append("MESG_DURATION_SEC>=0?EXIT")
            lines.append("")
            for sub in interval['subintervals']:
                lines.append("=SUBINTERVAL=")
                lines.append(f"INTERVAL_NAME={sub['name']}")
                lines.append(f"PERCENT_FTP_HI={sub['percent_ftp']}")
                lines.append(f"MESG_DURATION_SEC>={sub['duration']}?EXIT")
                lines.append("")
        else:
            lines.append("=INTERVAL=")
            lines.append(f"INTERVAL_NAME={interval['name']}")
            lines.append(f"PERCENT_FTP_HI={interval['percent_ftp']}")
            lines.append(f"MESG_DURATION_SEC>={interval['duration']}?EXIT")
            lines.append("")
    return '\n'.join(lines)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python yaml_to_plan.py input.yaml output.plan")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Add _generated_by_library suffix if not already present
    if not output_file.endswith('_generated_by_library.plan'):
        base_name = os.path.splitext(output_file)[0]
        output_file = f"{base_name}_generated_by_library.plan"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        yaml_data = yaml.safe_load(f)
    plan_text = yaml_to_plan(yaml_data)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(plan_text)
    print(f"Converted {input_file} to {output_file}")