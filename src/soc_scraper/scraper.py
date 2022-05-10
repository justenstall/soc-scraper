'''
scraper.py

Written by Justen Stall for University of Dayton Sociology Department

Usage
===================================
Usage: python3 scraper.py --help [for options]

Required Packages: see environment.yml for required packages

Description
===================================
This Main class is defined to efficently get the relevent words to search for, read files that may be relevant, and compare the two and compute a relevancy score

Class Attributes
===================================
newWordList --> The Word list, as a set of key value pairs
	- type: dictionary
documents --> self defined class, see documentation for further explanation in document.py
    -type: document
listOfWordCounts --> list containing the words of each document split on special characters and stripped for common words
    - type: list 
allWordCount --> a count of all the words that were parsed in a file/directory
    - int
idfs --> inverse document frequency, see http://www.tfidf.com/ for further info
    - type: dictionary
tf --> term frequency, see http://www.tfidf.com/ for further info
    - type: dictionary
tfidf --> term frequency - inverse document frequency model, the resulting relevancy score
    - type: dictionary
relevanceScore --> derived from the tf-idf model, a score given to a document based on its similarity to a predefined wordlist and other factors
    - type: float
'''
from typing import Optional
import typer
import facebook_scraper

app = typer.Typer()

@app.command()
def hello(name: Optional[str] = None):
    """
    Extra help text
    """
    if name:
        typer.echo(f"Hello {name}")
    else:
        typer.echo("Hello World!")


@app.command()
def bye(name: Optional[str] = None):
    if name:
        typer.echo(f"Bye {name}")
    else:
        typer.echo("Goodbye!")


@app.command()
def group(url: str = typer.Argument(...)):
    if url == None:
        return typer.Exit(code=128)
    
    for post in facebook_scraper.get_posts(
        'https://www.facebook.com/groups/babysleeptrainingtips', 
        # 'justenstall@gmail.com',
        group='babysleeptrainingtips',
        account=('justenstall@gmail.com', '7kd28w*Rdf9igzV8wYvH')):
        print(post['text'][:50])

    


if __name__ == "__main__":
    app()
