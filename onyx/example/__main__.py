import os, sys
from pathlib import Path


def run_example(name: str):
    ex_dir = os.path.join(Path(__file__).parents[2], "examples")
    if not os.path.isdir(ex_dir):
        print("Unable to find Onyx examples directory...")
        return

    examples = [
        *filter(
            lambda item: Path(item).suffix == ".py",
            os.listdir(ex_dir),
        )
    ]

    if name is None:
        match len(examples):
            case 0:
                print("No examples available...")
            case c:
                print(f"{c} example{'s' if c > 1 else ''} available:")
                for ex in examples:
                    print(f" - {ex}")
                print(f"Run `python -m onyx.example <name>` to run that example!")

    else:
        name = name if Path(name).suffix == ".py" else name + ".py"
        if name not in examples:
            print(f"Example {name} not found.")
            return

        print(f"Running example: {name}")
        os.system(f"python {os.path.join(ex_dir, name)}")


run_example(sys.argv[1] if len(sys.argv) > 1 else None)
