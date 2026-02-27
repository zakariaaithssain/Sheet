from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from rich import box

from agent.runtime import AgentRuntime
from config.settings import Settings

import logging 
import datetime


logger = logging.getLogger("interface")
console = Settings.console
console.set_window_title("Sheet, THE SHEET AGENT")





def start_api(agent_runtime:AgentRuntime):
        _render_banner()
        logger.debug("called Interface.start_api")
        with agent_runtime as runtime:
            logger.debug("inside runtime context manager")
            history_gen = None
            steps = 0 
            while True:
                user_input = ""
                while user_input == "": 
                    user_input = str(console.input())

                console.print()
                if user_input.lower().strip() == "q":
                    logger.info("user input was 'q', breaked from loop.")
                    break
                elif user_input.lower().strip() == "h": 
                    if history_gen is None: 
                         history_gen = runtime.history.load_conversations()
                    try:
                        console.print(Markdown("*history:* "))
                        row = next(history_gen)
                        console.print(f"{row['title']} - {row['created_at']}")
                    except StopIteration:
                        console.print("No more conversations.")
                        history_gen = None  # reset so next h starts over

                else:
                    #generate the title if first message
                    if steps == 0: 
                        runtime.step(user_input, first_message=True)
                    else: 
                         runtime.step(user_input)

                    steps+=1
                    logger.debug(f"step (1-indexed): {steps}")
                    console.print()





def _render_banner():
    logo_lines = [
        " ███████╗██╗  ██╗███████╗███████╗████████╗",
        " ██╔════╝██║  ██║██╔════╝██╔════╝╚══██╔══╝",
        " ███████╗███████║█████╗  █████╗     ██║   ",
        " ╚════██║██╔══██║██╔══╝  ██╔══╝     ██║   ",
        " ███████║██║  ██║███████╗███████╗   ██║   ",
        " ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝   ╚═╝   ",
    ]

    logo = Text()
    colors = ["#00E5FF", "#00D4F0", "#00C2E0", "#00B0D0", "#009EC0", "#008CB0"]
    for line, color in zip(logo_lines, colors):
        logo.append(line + "\n", style=f"bold {color}")

    #info block
    now = datetime.datetime.now()
    info = Text()
    info.append("\n")
    info.append("  Agent   ", style="bold #888888")
    info.append("Sheet v1.0.0\n", style="bold white")
    info.append("  Target  ", style="bold #888888")
    info.append("Monthly Budget\n", style="bold #00E5FF")
    info.append("  Source  ", style="bold #888888")
    info.append("Google Sheets\n", style="bold white")
    info.append("  Session ", style="bold #888888")
    info.append(f"{now.strftime('%Y-%m-%d  %H:%M:%S')}\n", style="dim white")

    #tip line
    tip = Text()
    tip.append("  - ", style="bold #FFD700")
    tip.append("Ask anything about your budget — Sheet will read, analyze, and update your spreadsheet.\n", style="dim white")
    tip.append("  - ", style="bold #FF6B6B")
    tip.append("Always review changes before confirming writes to your sheet.", style="dim white")

    #combine everything
    content = Text()
    content.append_text(logo)
    content.append("─" * 44 + "\n", style="dim #333333")
    content.append_text(info)
    content.append("─" * 44 + "\n", style="dim #333333")
    content.append_text(tip)
    content.append("\n")

    panel = Panel(
        content,
        box=box.HEAVY,
        border_style="#00E5FF",
        padding=(0, 1),
        subtitle="[dim]type [bold white]exit[/bold white] to quit  ·  [bold white]hist[/bold white] for history[/dim]",
        subtitle_align="center",
    )

    console.print()
    console.print(panel)
    console.print()
