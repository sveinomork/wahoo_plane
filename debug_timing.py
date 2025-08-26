#!/usr/bin/env python3
"""
Debug script for å sjekke timing av intervaller
"""

from plot_intervals import load_yaml_data, expand_intervals
import os

def main():
    """Debug timing med eksempel-filen"""
    yaml_file = "example/4x4-3-2-1.yaml"
    
    if not os.path.exists(yaml_file):
        print(f"Feil: Eksempelfilen '{yaml_file}' ble ikke funnet.")
        return
    
    # Last YAML-data
    yaml_data = load_yaml_data(yaml_file)
    
    print(f"=== ORIGINAL YAML DATA ===")
    for i, interval in enumerate(yaml_data['intervals']):
        if 'subintervals' in interval:
            repeat = interval.get('repeat', 1)
            print(f"{i+1}. {interval['name']}: (Repeat {repeat} times)")
            for j, sub in enumerate(interval['subintervals']):
                print(f"   {chr(97+j)}. {sub['name']}: {sub['duration']}s ({sub['duration']//60}:{sub['duration']%60:02d})")
        else:
            duration = interval['duration']
            print(f"{i+1}. {interval['name']}: {duration}s ({duration//60}:{duration%60:02d})")
    
    print(f"\n=== EXPANDED INTERVALS ===")
    expanded = expand_intervals(yaml_data)
    
    for i, interval in enumerate(expanded):
        start_min = interval['start_time'] // 60
        start_sec = interval['start_time'] % 60
        end_min = interval['end_time'] // 60
        end_sec = interval['end_time'] % 60
        duration_min = interval['duration'] // 60
        duration_sec = interval['duration'] % 60
        
        print(f"{i+1:2d}. {interval['name']:20s} | "
              f"{start_min:2d}:{start_sec:02d} - {end_min:2d}:{end_sec:02d} | "
              f"Varighet: {duration_min:2d}:{duration_sec:02d} | "
              f"{interval['percent_ftp']:3d}% FTP")

if __name__ == "__main__":
    main()
