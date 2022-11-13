"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Spyfi."""


if __name__ == "__main__":
    main(prog_name="spyfi")  # pragma: no cover
