import scratchattach
from requests import get
import time, os, traceback, random, json

api = "https://api.scratch.mit.edu"
session = scratchattach.login(os.getenv("USERNAME"), os.getenv("PASSWORD"))
user = session.get_linked_user()
add_projects = user.projects()
random.shuffle(add_projects)

def search(term=None):
    url = f"{api}/search/studios?q={term}" if term else f"{api}/search/studios"
    res = get(url).json()
    for studio in res:
        if not studio["open_to_all"]:
            continue
        yield studio["id"]
        
def connect_all(term=None):
    for studio in search(term):
        try:
            studio = session.connect_studio(studio)
            yield studio
        except:
            print(f"Failed to connect to {studio}")

def add_all(term=None, *, projects=None):
    projects = projects or add_projects
    for studio in connect_all(term):
        if not studio:
            continue
        if "undertale" in studio.description.lower() or "minecraft" in studio.description.lower():
            continue
        for project in random.sample(projects, 3) if len(projects) > 3 else projects:
            try:
                project = project.id
            except: 
                pass
            try:
                studio.remove_project(project)
                time.sleep(1+3*(random.random()**2))
                studio.add_project(project)
                time.sleep(3+3*(random.random()**2))
            except json.decoder.JSONDecodeError:
                print(f"Ratelimited at {studio.id}")
                exit()
            except Exception:
                print(f"Failed to access {studio.id if studio else None}")
                traceback.print_exc()
                

add_all("anything")
add_all("games")
add_all("cool games")
add_all("all projects")
add_all("everything")
add_all("best games")
add_all("good games")
add_all("whatever")
add_all("get this to")
add_all("10000 projects")
add_all("100000 projects")
