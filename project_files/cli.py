import sys
from tests.live_test            import Test
from project_files.manage_esp   import Esp
from project_files.animation    import ThinkingAnimation
from rich.console               import Console

anim = ThinkingAnimation()
console = Console()
esp = Esp("sketch")

user_input = ""

def cli():
    
    while True:
        console.print(f"[bold]OPTIONS[/][dim]   Enter: 1 to run tests.. and so on[/]")
        console.print(f"1. Run Tests")
        console.print(f"2. Compile ESP Firmware")
        console.print(f"3. Flash Firmware")
        console.print(f"[dim]0. Exit[/]")
        
        user_input = input(">>  ")
        if user_input == "0":
            sys.exit(1)
        elif user_input == "1":
            test = Test()
            test.test_report()
            test.close()
        elif user_input == "2":
            anim.start(action="Compiling...")
            result = esp.compile()
            anim.stop()
            console.print(f"[bold]RESULT:[/] [dim]{result.stdout}\nERROR: {result.stderr}\nRETURNCODE: {result.returncode}[/]")
            if result.returncode == 0:
                console.print(f"> [bold green]Compilation Succesfull[/]\n")
        elif user_input == "3":
            anim.start(action="Flashing Firmware...[press the boot button]")
            result = esp.flash()
            anim.stop()
            console.print(f"[bold]FLASH REPORT[/]\n[bold]OUTPUT[/]: {result.stdout}\n[bold]ERROR: [/]{result.stderr}")
            if result.returncode == 0:
                console.print(f"> [bold green]Flashing Succesfull.[/]\n")
    
    
if __name__ == "__main__":
    print("\n\n")
    cli()