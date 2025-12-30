import asyncio
from typing import Any
import requests
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, RichLog, Label, ProgressBar, Static, Button
from textual.containers import Horizontal, Vertical, Container
from textual.binding import Binding

from src.audio_synthesizer import AudioSynthesizer
from src.generator import Script_Generator
from src.niche_discovery import Niche_Discovery
from helpers.write_to_file import write_script_to_file

NEXUS_BRANDING = """
[bold #1e40af]███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗[/]
[bold #3b82f6]████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝[/]
[bold #06b6d4]██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗[/]
[bold #10b981]██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║[/]
[bold #22c55e]██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║[/]
[bold #4ade80]╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝[/]
"""

class NexusAutomation(App):
    TITLE = "NEXUS | YouTube Automation AI"
    CSS_PATH = "style/styles.tcss"

    BINDINGS = [
        Binding("d", "discover", "Discover", priority=True),
        Binding("q", "quit", "Quit", priority=True),
        Binding("r", "reset", "Reset", priority=False),
    ]

    def __init__(self):
        super().__init__()
        self.api_connected = None 

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id="main_container"):
            
            with Vertical(id="sidebar"):
                yield Label("DASHBOARD", classes="section-title")
                
                with Container(classes="stat-card"):
                    yield Label("API CONNECTION", classes="stat-label")
                    yield Static("Checking...", id="api_status")
                
                with Container(classes="stat-card"):
                    yield Label("SYSTEM STATUS", classes="stat-label")
                    yield Static("Ready", id="status_indicator")
                
                with Container(classes="stat-card"):
                    yield Label("FOUND", classes="stat-label")
                    yield Static("0", id="count_found", classes="stat-value")
                    yield Label("COMPLETED", classes="stat-label")
                    yield Static("0", id="count_done", classes="stat-value")
                
                yield Label("PROGRESS", classes="stat-label")
                yield ProgressBar(id="overall_progress", show_percentage=True)
            
            with Vertical(id="content_area"):
                yield Static(NEXUS_BRANDING, id="console_header")
                yield RichLog(id="process_log", markup=True)
                
                with Horizontal(id="button_row"):
                    yield Button("START DISCOVERY", id="btn_discover", variant="success")
                    yield Button("RESET LOGS", id="btn_reset", variant="primary")
                    yield Button("QUIT", id="btn_quit", variant="error")
        
        yield Footer()

    async def on_mount(self) -> None:
        self.query_one("#overall_progress").display = False
        log = self.query_one(RichLog)
        log.write("[bold #60a5fa]Welcome Back Jamie[/bold #60a5fa]\n")
        
        await self.check_api_connection()
        self.set_interval(10, self.check_api_connection)

    async def check_api_connection(self) -> None:
        """Polls the LLM server and updates the UI indicator."""
        status_widget = self.query_one("#api_status")
        try:
            response = await asyncio.to_thread(requests.get, "http://localhost:1234/v1/models", timeout=2)
            is_now_connected = (response.status_code == 200)
        except Exception:
            is_now_connected = False

        if is_now_connected:
            status_widget.update("[bold #4ade80]● ONLINE[/bold #4ade80]")
        else:
            status_widget.update("[bold #ef4444]● OFFLINE[/bold #ef4444]")
        
        self.api_connected = is_now_connected

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_discover":
            await self.action_discover()
        elif event.button.id == "btn_reset":
            self.action_reset()
        elif event.button.id == "btn_quit":
            await self.action_quit()

    def update_status(self, status: str, status_type: str = "ready") -> None:
        si = self.query_one("#status_indicator")
        si.update(status)
        si.remove_class("active")
        if status_type == "active": 
            si.add_class("active")

    async def action_discover(self):
        log = self.query_one(RichLog)
        if not self.api_connected:
            log.write("[#ef4444]Cannot start: LLM API is offline.[/#ef4444]\n")
            return

        self.update_status("Discovering...", "active")
        log.write("[bold]Niche Discovery Started...[/bold]\n")
        
        try:
            discovery = Niche_Discovery()
            niches = await asyncio.to_thread(discovery.get_niches, '')
            if niches:
                self.query_one("#count_found").update(str(len(niches)))
                await self.process_niches(niches)
        except Exception as e:
            log.write(f"[#ef4444]Error: {e}[/#ef4444]\n")
            self.update_status("Ready")

    async def process_niches(self, niches: list):
        log = self.query_one(RichLog)
        prog = self.query_one("#overall_progress")
        prog.display = True
        prog.total = len(niches)
        
        generator = Script_Generator()
        synthesizer = AudioSynthesizer()
        
        for i, niche in enumerate[Any](niches, 1):
            self.update_status(f"Processing: {niche}", "active")
            try:
                script = await asyncio.to_thread(generator.generate_script, '', niche)
                if write_script_to_file(niche, script):
                    safe_name = niche.replace(' ', '_').replace('-', '_').replace('/', '_')
                    await synthesizer.convert_text_to_voice(script, f"{safe_name}.txt")
                    log.write(f"[#4ade80]✓ {niche} complete.[/#4ade80]\n")
            except Exception as e:
                log.write(f"   [#ef4444]✗ Failed {niche}: {e}[/#ef4444]\n")
            
            prog.progress = i
            self.query_one("#count_done").update(str(i))
        
        self.update_status("Ready")

    def action_reset(self):
        self.query_one("#count_found").update("0")
        self.query_one("#count_done").update("0")
        self.query_one("#overall_progress").display = False
        self.query_one(RichLog).clear()
        self.update_status("Ready")

if __name__ == "__main__":
    app = NexusAutomation()
    app.run()