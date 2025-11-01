# Flask TODO App

## Introduction
The Flask TODO App is a lightweight task manager built with the Flask microframework and TinyDB, a document-oriented database stored as a local JSON file. The application demonstrates how to combine Flask routing, HTML templating, and client-side enhancements to provide a fully functional CRUD (Create, Read, Update, Delete) experience for managing personal to-do lists.

## Features
- **Task creation** – Add new tasks from the home page using an HTML form backed by a POST request to the `/add` route.
- **Task updates** – Modify task titles in place through a popup form that submits to the `/update` route.
- **Completion tracking** – Mark items as complete via the `/complete/<todo_id>` route; completed tasks are styled differently and displayed with strikethrough text.
- **Task deletion** – Remove tasks entirely by visiting the `/delete/<todo_id>` route.
- **Responsive UI** – Utilizes W3.CSS and Font Awesome to offer a polished, responsive user interface with real-time date and time display.

## Project Structure
```
.
├── app.py              # Flask application and TinyDB interactions
├── db.json             # TinyDB storage file created/maintained at runtime
├── requirements.txt    # Python dependencies for the project
├── templates/
│   └── index.html      # Jinja2 template rendering the to-do list UI
└── screenshot/         # Example UI screenshots
```

## Application Components
### `app.py`
The core Flask application defines routes for rendering the main page and handling CRUD operations:
- `root()` (`"/"`): Fetches documents from TinyDB, exposes TinyDB `doc_id` values as `id` fields, and renders `index.html` with the task list.
- `add()` (`"/add"`, POST): Reads the task title from the submitted form, inserts a new document with `complete: False`, and redirects to the home page.
- `update()` (`"/update"`, POST): Receives a task ID and updated title from the popup form, updates the corresponding TinyDB document, and redirects back to the main view.
- `delete(todo_id)` (`"/delete/<int:todo_id>"`): Removes the specified task from TinyDB.
- `complete(todo_id)` (`"/complete/<int:todo_id>"`): Sets the `complete` flag to `True` for the selected task.

### `templates/index.html`
The `index.html` template renders the user interface using W3.CSS components:
- Displays current date and time via a small JavaScript function that refreshes every second.
- Provides a form for adding tasks, linked to the `/add` endpoint.
- Iterates over `todo_list` to render tasks with conditional styling based on completion state, including buttons for marking complete, editing (popup), and deleting.
- Contains a hidden popup form with fields for editing task titles. When triggered, JavaScript populates the form with the current title and task ID before submitting to `/update`.

### `db.json`
TinyDB persists data in `db.json`. The file is created automatically the first time the application inserts data; you do not need to create it manually. Avoid editing this file directly to maintain data integrity.

## Prerequisites
- Python 3.8 or newer
- `pip` for dependency management

## Setup Instructions
1. **Create and activate a virtual environment (recommended):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application
1. **Start the Flask development server:**
   ```bash
   flask --app app run --debug
   ```
   Alternatively, you can run `python app.py` to start the server with `debug=True`.
2. **Open the application in your browser:** Navigate to `http://127.0.0.1:5000/` to view and interact with the to-do list.

## How It Works
1. When the home page loads, `root()` queries TinyDB for all tasks, attaches their `doc_id`, and passes the list to the template.
2. Submitting the add form posts a new task to TinyDB, then redirects to the refreshed task list.
3. Clicking the edit icon opens a popup populated with the existing task title; submitting the popup sends an update request.
4. Marking a task complete sets its `complete` flag, altering its display style.
5. Deleting a task removes the record entirely.

## Development Tips
- TinyDB stores data in JSON format. For bulk updates or resets, consider deleting `db.json`; the application will recreate it.
- Debug logging can be enabled by setting `FLASK_ENV=development` or using `flask run --debug` for more verbose output.
- To customize the UI, edit `templates/index.html` and optionally add static assets (CSS/JS) via Flask's `static` folder pattern.

## Screenshots
Example screenshots are available in the `screenshot/` directory, demonstrating the home view and CRUD interactions.

## License
This project is provided for educational purposes. Refer to the repository details for licensing information or adapt as needed.
