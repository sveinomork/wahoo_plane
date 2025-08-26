
import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
import yaml
import os
from .yaml_to_plan import yaml_to_plan
from .plot_intervals import plot_intervals, load_yaml_data
from .interactive_workout import build_workout_interactively

import platform

console = Console()

# Disable emojis on Windows
if platform.system() == "Windows":
    EMOJI_ROCKET = ""
    EMOJI_WORKOUT = ""
    EMOJI_SUCCESS = ""
else:
    EMOJI_ROCKET = "🚀"
    EMOJI_WORKOUT = "🏋️‍♀️"
    EMOJI_SUCCESS = "🎉"

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """A CLI to generate Wahoo .plan files and interval plots."""
    if ctx.invoked_subcommand is None:
        generate()
    pass

@cli.command()
def generate():
    """Generate a .plan file and a plot from a YAML file or interactively."""
    console.print(Panel(f"{EMOJI_ROCKET} Wahoo Workout Generator {EMOJI_ROCKET}", title="[bold green]Wahoo Workout Generator[/bold green]"))
    
    if Confirm.ask("Generate workout from a file?", default=True):
        yaml_file = Prompt.ask("Enter the path to the YAML file")
        try:
            # Load YAML data
            yaml_data = load_yaml_data(yaml_file)
            
            # Generate .plan file
            plan_text = yaml_to_plan(yaml_data)
            base_name = os.path.splitext(yaml_file)[0]
            plan_file = f"{base_name}.plan"
            with open(plan_file, 'w', encoding='utf-8') as f:
                f.write(plan_text)
            console.print(f"✅ Successfully generated .plan file: [bold green]{plan_file}[/bold green]")
            
            # Generate plot
            plot_file = f"{base_name}.png"
            plot_intervals(yaml_data, save_file=plot_file, show_plot=False)
            console.print(f"✅ Successfully generated plot: [bold green]{plot_file}[/bold green]")
            
            console.print(Panel(f"{EMOJI_SUCCESS} Workout generation complete! {EMOJI_SUCCESS}", title="[bold green]Success[/bold green]"))
            
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
    else:
        workout_data = build_workout_interactively()
        try:
            # Generate .plan file
            plan_text = yaml_to_plan(workout_data)
            base_name = workout_data['name'].lower().replace(' ', '_')
            plan_file = f"{base_name}.plan"
            with open(plan_file, 'w', encoding='utf-8') as f:
                f.write(plan_text)
            console.print(f"✅ Successfully generated .plan file: [bold green]{plan_file}[/bold green]")
            
            # Generate plot
            plot_file = f"{base_name}.png"
            plot_intervals(workout_data, save_file=plot_file, show_plot=False)
            console.print(f"✅ Successfully generated plot: [bold green]{plot_file}[/bold green]")
            
            console.print(Panel(f"{EMOJI_SUCCESS} Workout generation complete! {EMOJI_SUCCESS}", title="[bold green]Success[/bold green]"))
            
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")


if __name__ == "__main__":
    cli()
