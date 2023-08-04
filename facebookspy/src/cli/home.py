from rich import box
from rich import print as rprint
from rich.layout import Layout
from rich.panel import Panel
from .baner import print_banner
from rich.console import Console


def display_start_menu() -> None:
    console = Console()
    print_banner(console)
    layout = Layout()
    header_content = Panel(
        renderable="🕵️ [gold1 bold]Facebook spy[/gold1 bold] allows you to log in and scrape information from facebook accounts just with a few clicks. Data are saved to database and then you can easly browse them from your local web application. \n\n🖥️ I am still working on developing more functions and making easy to use application. ",
        title="[reverse]ABOUT Facebook Spy[/reverse]",
        title_align="center",
        border_style="bold green",
        padding=(1, 1),
        box=box.DOUBLE_EDGE,
        highlight=True,
    )

    footer_content = Panel(
        renderable="\n    👩‍💻 [b reverse]Source[/b reverse]: [link=https://github.com/DEENUU1/facebook-spy]GitHub[/link]\t\t\t    📚 [b reverse]Docs[/b reverse]: [link=https://github.com/DEENUU1/facebook-spy/blob/main/README.md]Read[/link]\t\t\t   🌐 [b reverse]Website (in develop) [/b reverse]: [link=...]Explore[/link]\t\t\t",
        title="[reverse]THANK YOU FOR USING THIS APP[/reverse]",
        title_align="center",
        border_style="bold violet",
        padding=(1, 0),
        box=box.DOUBLE_EDGE,
        highlight=True,
    )

    main_content = Panel(
        renderable="[bold green]1.[/bold green] Log in with/without 2-step verification\n[bold green]2.[/bold green] Scrape basic information from facebook account (fullname, list of friends, places, work and education, family members) \n[bold green]3.[/bold green] Scraping and downloading images from facebook account\n[bold green]4.[/bold green] Extracting urls to reels and videos from facebook account\n[bold green]5.[/bold green] Saving all scraped data to database (sqlite)\n[bold green]6.[/bold green] FastAPI server to browse scraped data\n[bold greem]7.[/bold greed] React app to browse scraped data",
        title="[reverse]FEATURES[/reverse]",
        title_align="center",
        border_style="bold blue",
        padding=(1, 1),
        box=box.DOUBLE_EDGE,
    )

    # Divide the "screen" in to three parts
    layout.split(
        Layout(name="header", size=14),
        Layout(name="main", size=18),
        Layout(name="footer", size=6),
    )

    # HEADER
    layout["header"].update(header_content)

    # MAIN CONTENT
    layout["main"].split_row(
        Layout(
            name="side",
        ),
        Layout(main_content, name="body", ratio=2),
    )

    # SIDE CONTENT
    layout["side"].split(
        # SIDE CONTENT TOP
        Layout(
            Panel(
                renderable="\t\t  💲💲💲 \n\n              EVERYBODY LIES      \n\n              GREGORY HOUSE\n\n \t\t  💰💰💰",
                border_style="green",
            )
        ),
        # SIDE CONTENT BOTTOM
        Layout(
            Panel(
                "🐍 [b u]Developed with[/b u]: Python, FastAPI, Typer, Rich, PyTest, Selenium, SQLite\n\n😎 [b u]Copyright[/b u]: 2023 (Kacper Wlodarczyk)\n\n✅ [b u]Language Support[/b u]: English, Polish",
                border_style="red",
            )
        ),
    )

    # FOOTER
    layout["footer"].update(footer_content)

    rprint(layout)
