from __future__ import print_function
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from todoist_api_python.api import TodoistAPI
from utils import credentials_handler
import json


def todoist_token_retriever():
    with open("todoist_token.json", "r") as f:
        todo_token = json.load(f)
    todo_token = todo_token["token"]
    return todo_token


todo_token = todoist_token_retriever()
api = TodoistAPI(todo_token)
SCOPES = ["https://www.googleapis.com/auth/tasks"]


def get_tasks_todoist():
    all_tasks = api.get_tasks()
    tasks = []
    # TODO: handler of recurrent event
    for task in all_tasks:
        try:
            print(task)
            print("\n")
            if task.due.datetime != None:
                tasks.append(task)
        except AttributeError:
            continue
    return tasks


# If modifying these scopes, delete the file token.json.


def set_tasks_on_gcal(tasks):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    creds = credentials_handler(SCOPES)
    try:
        service = build("tasks", "v1", credentials=creds)

        # Call the Calendar API
        for task in tasks:
            event_details = {
                "updated": task.created,
                "title": task.content,
                "due": task.due.datetime + "Z",
                "notes": task.description,
                "id": str(task.id),
            }
            # I have to put the task in the correct spot
            event = (
                service.tasks()
                .insert(
                    tasklist="@default",
                    body=event_details,
                )
                .execute()
            )
    except HttpError as error:
        print("An error occurred: %s" % error)
    return event


def main():
    tasks = get_tasks_todoist()
    # set_tasks_on_gcal(tasks)


if __name__ == "__main__":
    main()
