#!/usr/bin/env python3
"""
Test script for å demonstrere plotting av intervalltrening
"""

from plot_intervals import load_yaml_data, plot_intervals
import os

def main():
    """Test plotting med eksempel-filen"""
    # Bruk eksempelfilen
    yaml_file = "example/4x4-3-2-1.yaml"
    
    if not os.path.exists(yaml_file):
        print(f"Feil: Eksempelfilen '{yaml_file}' ble ikke funnet.")
        print("Sørg for at du kjører scriptet fra riktig mappe.")
        return
    
    try:
        # Last YAML-data
        print(f"Laster treningsdata fra: {yaml_file}")
        yaml_data = load_yaml_data(yaml_file)
        
        print(f"Treningsnavn: {yaml_data['name']}")
        print(f"Varighet: {yaml_data['duration']} sekunder ({yaml_data['duration']//60} minutter)")
        print(f"TSS: {yaml_data['tss']}")
        print(f"IF: {yaml_data['if']}")
        
        # Lag plottet (vis bare på skjermen)
        print("\nGenererer plot...")
        plot_intervals(yaml_data, save_file="workout_example.png", show_plot=False)
        print("Plot ferdig! Sjekk filen 'workout_example.png'")
        
    except Exception as e:
        print(f"Feil ved plotting: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
