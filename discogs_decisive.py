# pip install discogs_client

import discogs_client
import random

import six
import inquirer
from pyfiglet import figlet_format

try:
    from termcolor import colored
except ImportError:
    colored = None


def cli_print(string, color, font="chunky", figlet=False):
    if colored:
        if not figlet:
            six.print_(colored(string, color))
        else:
            six.print_(colored(figlet_format(string, font=font), color))
    else:
        six.print_(string)


def generate_albums(genre_selection):
    # INPUT YOUR DISCOGS USER TOKEN!
    discogs_user_token = ""
    if discogs_user_token == "":
        exit("Please input your user token.")

    # initialize user token
    dc = discogs_client.Client("discogs-decisive/0.1 +http://github.com/danpops",
                               user_token=discogs_user_token)
    me = dc.identity()

    # access collection uncategorized folder
    items_in_collection = [r.release for r in me.collection_folders[0].releases]

    # initialize rows array to store collection
    rows = []

    # create a dict for each release in collection
    for r in items_in_collection:
        row = {}

        try:
            row['primaryGenre'] = r.genres[0]
            if len(r.genres) > 1:  # if album has more than 1 genre
                row['secondaryGenres'] = ", ".join(r.genres[1:])

            row['catalogNumber'] = r.labels[0].data['catno']
            row['artists'] = ", ".join(a.name for a in r.artists)
            row['format'] = r.formats[0]['descriptions'][0]

        except (IndexError, TypeError):
            None
            # ideally, these exceptions only occur when data is missing
            # but usually the program checks if values are missing, rather than
            # ignoring any exception resulting from trying

        row['title'] = r.title

        if r.year > 0:
            row['year'] = r.year

        rows.append(row)

    genre_selected_albums = []

    # loops through collection to check if release matches
    # user selected genre, verifies if there is an artist
    # and album title.
    # it will then check if it is an LP release and not a
    # CD or other.
    for row in rows:
        if genre_selection in row.values():
            if (row.get('artists') or row.get("title")) != "":
                if row.get('format') == ("LP" or "12\""):
                    genre_selected_albums.append(row)

    # randomly select THREE albums from user selected category
    five_random_albums = []
    i = 1
    while i <= 3:
        choice = random.choice(genre_selected_albums)
        print()
        cli_print("Album {}".format(i), "red")
        cli_print("Artist: " + choice.get('artists'), "blue")
        cli_print("Album: " + choice.get('title'), "blue")
        i += 1


def main():
    """
    Generate 3 random albums from your collection to listen
    to, categorized by genre.
    Trust me. I never can decide what to listen to in my record
    collection. Python and Discogs made it a little easier.
    Happy collecting :)
    """
    cli_print("*-----------------------------------------------------------*", "blue")
    cli_print("__discogs decisive__", color="green", figlet=True)
    cli_print("*-----------------------------------------------------------*", "blue")
    cli_print("*----------* deciding what to spin next is hard. *----------*", "blue")
    cli_print("*-------*  when you don't know what to pick, we do. *-------*", "blue")
    cli_print("*-----------------------------------------------------------*", "blue")
    cli_print("", color="green", figlet=True)

    questions = [
        inquirer.List(
            "genre_pick",
            message="Pick the genre you want to listen to [use arrow keys]",
            choices=["Rock", "Hip Hop", "Electronic", "Jazz", "Other"],
        ),
    ]

    answers = inquirer.prompt(questions)
    genre = answers.get('genre_pick')

    cli_print("Hang tight! We're grabbing your three records...", "green")

    generate_albums(genre)
    print()
    cli_print("Happy collecting :)", "green")


if __name__ == "__main__":
    main()
