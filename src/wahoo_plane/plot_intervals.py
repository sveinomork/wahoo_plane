import yaml
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

def load_yaml_data(yaml_file):
    """Laster YAML-data fra fil"""
    with open(yaml_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def expand_intervals(yaml_data):
    """Ekspanderer intervaller med repetitions til en flat liste"""
    expanded = []
    current_time = 0
    
    for interval in yaml_data['intervals']:
        if 'subintervals' in interval:
            # Håndter repeterende subintervaller
            repeat_count = interval.get('repeat', 1)
            for rep in range(repeat_count):
                for sub in interval['subintervals']:
                    expanded.append({
                        'name': f"{sub['name']}" + (f" ({rep+1}/{repeat_count})" if repeat_count > 1 else ""),
                        'percent_ftp': sub['percent_ftp'],
                        'duration': sub['duration'],
                        'start_time': current_time,
                        'end_time': current_time + sub['duration']
                    })
                    current_time += sub['duration']
        else:
            # Vanlig intervall
            expanded.append({
                'name': interval['name'],
                'percent_ftp': interval['percent_ftp'],
                'duration': interval['duration'],
                'start_time': current_time,
                'end_time': current_time + interval['duration']
            })
            current_time += interval['duration']
    
    return expanded

def get_color_for_intensity(percent_ftp):
    """Returnerer farge basert på intensiteten (% av FTP)"""
    if percent_ftp <= 55:
        return '#2E8B57'  # Grønn - Recovery/Active Recovery
    elif percent_ftp <= 75:
        return '#4169E1'  # Blå - Endurance
    elif percent_ftp <= 90:
        return '#FF8C00'  # Orange - Tempo
    elif percent_ftp <= 105:
        return '#FF4500'  # Rød-orange - Threshold
    elif percent_ftp <= 120:
        return '#DC143C'  # Rød - VO2 Max
    else:
        return '#8B008B'  # Mørk magenta - Neuromuscular/Anaerobic

def format_time(seconds):
    """Formaterer sekunder til mm:ss format"""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes}:{seconds:02d}"

def plot_intervals(yaml_data, save_file=None, show_plot=True):
    """Plotter intervalltrening som stolpediagram"""
    expanded_intervals = expand_intervals(yaml_data)
    
    # Sett opp figuren
    plt.figure(figsize=(14, 8))
    
    # Hent data for plotting
    start_times = [interval['start_time'] for interval in expanded_intervals]
    durations = [interval['duration'] for interval in expanded_intervals]
    intensities = [interval['percent_ftp'] for interval in expanded_intervals]
    names = [interval['name'] for interval in expanded_intervals]
    colors = [get_color_for_intensity(intensity) for intensity in intensities]
    
    # Konverter til minutter for bedre lesbarhet
    start_times_min = [t/60 for t in start_times]
    durations_min = [d/60 for d in durations]
    
    # Lag stolpediagrammet - plasser stolper med riktig alignment
    bars = plt.bar(start_times_min, intensities, width=durations_min, 
                   color=colors, alpha=0.8, edgecolor='black', linewidth=0.5,
                   align='edge')  # Viktig: align='edge' sørger for riktig plassering
    
    # Legg til labels på hver stolpe
    for i, (bar, name, intensity) in enumerate(zip(bars, names, intensities)):
        height = bar.get_height()
        x_pos = bar.get_x() + bar.get_width()/2
        
        # Plasser tekst i midten av stolpen hvis den er høy nok, ellers over
        if height > 20:
            y_pos = height / 2
            color = 'white'
            weight = 'bold'
        else:
            y_pos = height + 2
            color = 'black'
            weight = 'normal'
        
        # Vis intensitet og navn (forkortet hvis for lang)
        label = f"{intensity}%\n{name[:12]}" if len(name) > 12 else f"{intensity}%\n{name}"
        plt.text(x_pos, y_pos, label, ha='center', va='center' if height > 20 else 'bottom',
                fontsize=8, color=color, weight=weight)
    
    # Tilpass aksene
    plt.xlabel('Tid (minutter)', fontsize=12)
    plt.ylabel('Intensitet (% FTP)', fontsize=12)
    plt.title(f'{yaml_data["name"]} - Intervalltrening\n'
              f'Varighet: {format_time(yaml_data["duration"])}, TSS: {yaml_data["tss"]}, IF: {yaml_data["if"]}', 
              fontsize=14, fontweight='bold')
    
    # Sett y-akse grenser
    plt.ylim(0, max(intensities) * 1.1)
    
    # Sett x-akse grenser og ticks
    total_duration_min = max([interval['end_time'] for interval in expanded_intervals]) / 60
    plt.xlim(0, total_duration_min)
    
    # Lag ticks for hver 5. eller 10. minutt avhengig av total varighet
    if total_duration_min <= 30:
        x_ticks = np.arange(0, total_duration_min + 1, 5)
    else:
        x_ticks = np.arange(0, total_duration_min + 1, 10)
    plt.xticks(x_ticks)
    
    # Legg til rutenett både x og y
    plt.grid(True, alpha=0.3, axis='both')
    
    # Legg til legende for intensitetssoner
    legend_elements = [
        plt.Rectangle((0,0),1,1, facecolor='#2E8B57', alpha=0.8, label='Recovery (≤55%)'),
        plt.Rectangle((0,0),1,1, facecolor='#4169E1', alpha=0.8, label='Endurance (56-75%)'),
        plt.Rectangle((0,0),1,1, facecolor='#FF8C00', alpha=0.8, label='Tempo (76-90%)'),
        plt.Rectangle((0,0),1,1, facecolor='#FF4500', alpha=0.8, label='Threshold (91-105%)'),
        plt.Rectangle((0,0),1,1, facecolor='#DC143C', alpha=0.8, label='VO2 Max (106-120%)'),
        plt.Rectangle((0,0),1,1, facecolor='#8B008B', alpha=0.8, label='Anaerobic (>120%)')
    ]
    plt.legend(handles=legend_elements, loc='upper right', fontsize=9)
    
    # Tilpass layout
    plt.tight_layout()
    
    # Lagre eller vis plot
    if save_file:
        plt.savefig(save_file, dpi=300, bbox_inches='tight')
        print(f"Plot lagret som: {save_file}")
    
    if show_plot:
        plt.show()

def main():
    """Hovedfunksjon"""
    if len(sys.argv) < 2:
        print("Bruk: python plot_intervals.py <yaml_fil> [output_image]")
        print("Eksempel: python plot_intervals.py example/4x4-3-2-1.yaml workout_plot.png")
        sys.exit(1)
    
    yaml_file = sys.argv[1]
    
    if not os.path.exists(yaml_file):
        print(f"Feil: Filen '{yaml_file}' ble ikke funnet.")
        sys.exit(1)
    
    try:
        # Last YAML-data
        yaml_data = load_yaml_data(yaml_file)
        
        # Bestem output-fil hvis spesifisert
        save_file = None
        if len(sys.argv) >= 3:
            save_file = sys.argv[2]
        
        # Lag plottet
        plot_intervals(yaml_data, save_file=save_file)
        
    except Exception as e:
        print(f"Feil ved plotting: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
