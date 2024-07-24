from typing import Any, List
from rich.table import Table
from rich.console import Console



class TableManager:
    def __init__(
        self,
    ):
        pass

    def display_table(self, title: str, items: list[dict], headers: list = None):
        """display table data with ritch table"""
        print('\n')
        table = Table(title=title,
                      padding=(0, 1),
                      header_style="blue",
                      title_style="purple",
                      min_width=60
                      )

        if not headers:
            try:
                headers = list(items[0].keys())
            except IndexError:
                headers = []
        for title in headers:
            table.add_column(str(title), justify="center", style="cyan")

        for item in items:
            values = [str(item.get(header, '')) for header in headers]
            table.add_row(*values)
            
        console = Console()
        print("")
        console.print(table)
