def print_section(title: str, data: dict) -> None:
    print(f"\n{title}")
    print("-" * len(title))
    for key, value in data.items():
        if isinstance(value, float):
            print(f"{key}: {value:,.6f}")
        else:
            print(f"{key}: {value}")