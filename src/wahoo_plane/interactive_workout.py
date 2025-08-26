
from rich.console import Console
from rich.prompt import Prompt, IntPrompt, Confirm
import platform

console = Console()

# Disable emojis on Windows
if platform.system() == "Windows":
    EMOJI_WORKOUT = ""
else:
    EMOJI_WORKOUT = "🏋️‍♀️"

def get_interval_details():
    """Get details for a single interval."""
    name = Prompt.ask("Enter interval name (e.g., 'Work', 'Rest')")
    duration = IntPrompt.ask("Enter duration in minutes")
    intensity = IntPrompt.ask("Enter intensity (% FTP)")
    return {"name": name, "duration": duration * 60, "percent_ftp": intensity}

def calculate_tss(intervals):
    """Calculate the TSS for a workout."""
    total_tss = 0
    for interval in intervals:
        if 'subintervals' in interval:
            repeat = interval.get('repeat', 1)
            for _ in range(repeat):
                for sub in interval['subintervals']:
                    duration_in_hours = sub['duration'] / 3600
                    intensity = sub['percent_ftp'] / 100
                    total_tss += duration_in_hours * (intensity ** 2) * 100
        else:
            duration_in_hours = interval['duration'] / 3600
            intensity = interval['percent_ftp'] / 100
            total_tss += duration_in_hours * (intensity ** 2) * 100
    return round(total_tss)

def build_workout_interactively():
    """Build a workout interactively."""
    workout = {"intervals": []}
    total_duration = 0

    console.print(f"--- {EMOJI_WORKOUT} Let's build a workout! ---")

    # Get workout name
    workout['name'] = Prompt.ask("Enter the name of your workout")

    # Get warm-up
    console.print("--- Warm-up ---")
    warmup_duration = IntPrompt.ask("Enter warm-up duration in minutes")
    warmup_intensity = IntPrompt.ask("Enter warm-up intensity (% FTP)")
    workout["intervals"].append({
        "name": "Warm-up",
        "duration": warmup_duration * 60,
        "percent_ftp": warmup_intensity
    })
    total_duration += warmup_duration * 60

    # Get interval blocks
    console.print("--- Interval Blocks ---")
    while Confirm.ask("Add an interval block?", default=True):
        block_name = Prompt.ask("Enter a name for this block (e.g., 'VO2 Max Intervals')")
        repetitions = IntPrompt.ask("How many times to repeat this block?", default=1)
        rest_duration = 0
        if repetitions > 1:
            rest_duration = IntPrompt.ask("Enter rest duration between blocks in minutes", default=0)
        
        subintervals = []
        while Confirm.ask("Add a sub-interval to this block?", default=True):
            subintervals.append(get_interval_details())
        
        if subintervals:
            if rest_duration > 0:
                subintervals.append({
                    "name": "Rest",
                    "duration": rest_duration * 60,
                    "percent_ftp": 50
                })
            workout["intervals"].append({
                "name": block_name,
                "repeat": repetitions,
                "subintervals": subintervals
            })
            block_duration = sum(sub['duration'] for sub in subintervals) * repetitions
            total_duration += block_duration

    # Get cool-down
    console.print("--- Cool-down ---")
    cooldown_duration = IntPrompt.ask("Enter cool-down duration in minutes")
    cooldown_intensity = IntPrompt.ask("Enter cool-down intensity (% FTP)")
    workout["intervals"].append({
        "name": "Cool-down",
        "duration": cooldown_duration * 60,
        "percent_ftp": cooldown_intensity
    })
    total_duration += cooldown_duration * 60

    # Calculate total duration, TSS, and IF
    workout['duration'] = total_duration
    workout['tss'] = calculate_tss(workout['intervals'])
    workout['if'] = round((workout['tss'] / (total_duration / 3600) / 100) ** 0.5, 2) if total_duration > 0 else 0

    return workout
