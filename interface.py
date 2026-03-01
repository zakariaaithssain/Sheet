from rich.panel import Panel
from rich.text import Text
from rich import box

from agent.runtime import AgentRuntime
from config.settings import Settings

import logging 
import datetime


logger = logging.getLogger("interface")
console = Settings.console
QUIT_STR = "/quit"


class Interface:
    def __init__(self):
        self.logger = logger
        self.console = console
        self.console.set_window_title("SHEET")
        self.quit_str = QUIT_STR

    def start_api(self, agent_runtime: AgentRuntime):
        self.logger.debug("called Interface.start_api")

        with agent_runtime as runtime:
            self.logger.debug("inside runtime context manager")
            steps = 0 
            while True:
                
                user_input = ""
                while user_input == "": 
                    user_input = self.console.input("❯ ")

                self.console.print()
                if user_input.lower().strip() == self.quit_str:
                    self.logger.info("user input was '/quit', breaked from loop.")
                    break
                else:
                    #generate the title if first message
                    if steps == 0: 
                        runtime.step(user_input, first_message=True)
                    else: 
                         runtime.step(user_input)

                    steps+=1
                    self.logger.debug(f"step (1-indexed): {steps}")
                    self.console.print()




    def render_banner(self):
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
        tip.append("Always review changes before confirming edits to your sheet.", style="dim white")

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
            subtitle=f"[dim]type [bold white]{self.quit_str}[/bold white] to quit",
            subtitle_align="center",
        )

        self.console.print()
        self.console.print(panel)
        self.console.print()
        self.logger.info("banner rendered.")





