import csv
import sys
import numpy as np
from util import  Node,StackFrontier,QueueFrontier



# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)
    print(path)
    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    source and tardet which goes into the function are already id number
    """

    # starting position


    if target in neighbors_for_person(source):
       return 1

    start = Node(state=source,parent=None,action=None)
    target_neighbors = list(neighbors_for_person(target))
    target_neighbors_actors=[]
    target_neighbors_movies=[]

    for i in range (len(target_neighbors)):
        target_neighbors_actors.append(target_neighbors[i][1])
        target_neighbors_movies.append(target_neighbors[i][0])
    print(target_neighbors_movies)
    print(target_neighbors_actors)

    frontier = QueueFrontier()
    frontier.add(start)
    explored_actors = set()
    while True:
        if frontier.empty():
            raise Exception("no solution")
        node = frontier.remove()
        # explored_actors.append(node.state)


        # If our node is a solution
        if node.state==target or (node.state in target_neighbors_actors)==True:
            movies = []
            src = []

            if (node.state in target_neighbors_actors)==True:
                src.append(target)
                last_movie = target_neighbors_movies[target_neighbors_actors.index(node.state)]
                movies.append(last_movie)

            # if frontier.contains_state(target):

            while node.parent is not None:
                movies.append(node.action)
                src.append(node.state)
                node = node.parent



            movies.reverse()
            src.reverse()
            # movies.append(lastpiece(target, src[0]))
            # src.append(target)
            path = list(zip(movies,src))
            return path

        # if it isn't a solution
        explored_actors.add(node.state)

        # continuing the search
        for movie, state in neighbors_for_person(node.state):
            if not frontier.contains_state(state) and state not in explored_actors:
                child = Node(state=state, parent=node, action=movie)
                frontier.add(child)


    #else:

    # TODO
    # raise NotImplementedError


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors

def lastpiece(target, last):
    movies,people = map(list, zip(*list(neighbors_for_person(target))))
    last_movie = movies[people.index(last)]
    return last_movie

if __name__ == "__main__":
    main()

