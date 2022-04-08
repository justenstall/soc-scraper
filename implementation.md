# Implementation Ideas

## CLI

I think a CLI will be the easiest way to get this working in a packageable way, even though it will take a learning curve for researchers. With a well-made CLI, the door is open for graphical user interfaces in the future which would be more user-friendly.

Previously, I have used the [click package](https://click.palletsprojects.com/en/8.1.x/). It was a good experience, but definitely had some room for improvement.

There is a newer package built on top of Click called Typer, that I am going to try using for this project.

[Typer Docs](https://typer.tiangolo.com/typer-cli/)

[Typer Repository](https://github.com/tiangolo/typer)

## Scraping

The goal is to use an open-source Facebook scraper for simplicity.

Open source scraper options:

- [facebook-scraper](https://github.com/kevinzg/facebook-scraper)
  - Most popular option on GitHub
  - Seems full featured
  - Provides a CLI
- [facebook-post-scraper](https://github.com/brutalsavage/facebook-post-scraper)
  - Contains limited comments support
