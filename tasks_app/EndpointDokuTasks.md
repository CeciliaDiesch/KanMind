1. GET
   /api/tasks/assigned-to-me/
   Description: Ruft alle Tasks ab, die dem aktuell authentifizierten Benutzer entweder als Bearbeiter (`assignee`) zugewiesen sind. Der Benutzer muss eingeloggt sein, um auf diese Tasks zuzugreifen.
   Request Body

{

}

Success Response
Die Antwort enthält eine Liste der Tasks, die entweder dem aktuell authentifizierten Benutzer zugewiesen wurden. Jede Task enthält grundlegende Informationen wie Titel, Status, Priorität und Fälligkeitsdatum.

[
{
"id": 1,
"board": 1,
"title": "Task 1",
"description": "Beschreibung der Task 1",
"status": "to-do",
"priority": "high",
"assignee": {
"id": 13,
"email": "marie.musterfraun@example.com",
"fullname": "Marie Musterfrau"
},
"reviewer": {
"id": 1,
"email": "max.mustermann@example.com",
"fullname": "Max Mustermann"
},
"due_date": "2025-02-25",
"comments_count": 0
},
{
"id": 2,
"board": 12,
"title": "Task 2",
"description": "Beschreibung der Task 2",
"status": "in-progress",
"priority": "medium",
"assignee": {
"id": 13,
"email": "marie.musterfraun@example.com",
"fullname": "Marie Musterfrau"
},
"reviewer": null,
"due_date": "2025-02-20",
"comments_count": 0
}
]

Status Codes

    200: Erfolgreich. Gibt eine Liste der Tasks zurück, die dem aktuell authentifizierten Benutzer entweder als Bearbeiter oder als Prüfer zugewiesen sind.
    401: Nicht autorisiert. Der Benutzer muss eingeloggt sein, um auf diese Tasks zugreifen zu können.
    500: Interner Serverfehler.

Rate Limits

    No limit

Permissions required: Der Benutzer muss eingeloggt und authentifiziert sein, um auf die Tasks zuzugreifen, die ihm als Bearbeiter (`assignee`) zugewiesen sind.

2. GET
   /api/tasks/reviewing/
   Description: Ruft alle Tasks ab, bei denen der aktuell authentifizierte Benutzer als Prüfer (`reviewer`) eingetragen ist. Der Benutzer muss eingeloggt sein, um auf diese Tasks zuzugreifen.
   Request Body

{

}

Success Response
Die Antwort enthält eine Liste der Tasks, die dem authentifizierten Benutzer zur Überprüfung zugewiesen wurden. Jede Task enthält grundlegende Informationen wie Titel, Status, Priorität und Fälligkeitsdatum.

[
{
"id": 1,
"board": 1,
"title": "Task 1",
"description": "Beschreibung der Task 1",
"status": "to-do",
"priority": "high",
"assignee": null,
"reviewer": {
"id": 1,
"email": "max.mustermann@example.com",
"fullname": "Max Mustermann"
},
"due_date": "2025-02-25",
"comments_count": 0
},
{
"id": 2,
"board": 12,
"title": "Task 2",
"description": "Beschreibung der Task 2",
"status": "in-progress",
"priority": "medium",
"assignee": {
"id": 13,
"email": "marie.musterfraun@example.com",
"fullname": "Marie Musterfrau"
},
"reviewer": {
"id": 1,
"email": "max.mustermann@example.com",
"fullname": "Max Mustermann"
},
"due_date": "2025-02-20",
"comments_count": 0
}
]

Status Codes

    200: Erfolgreich. Gibt eine Liste der Tasks zurück, bei denen der Benutzer als Prüfer (`reviewer`) eingetragen ist.
    401: Nicht autorisiert. Der Benutzer muss eingeloggt sein, um auf diese Tasks zugreifen zu können.
    500: Interner Serverfehler.

Rate Limits

    No limit

Permissions required: Der Benutzer muss eingeloggt und authentifiziert sein, um auf die Tasks zuzugreifen, die ihm als Prüfer (`reviewer`) zugewiesen sind.

3.

POST
/api/tasks/
Description: Erstellt eine neue Task innerhalb eines Boards. Der Benutzer muss einen der folgenden Werte für den Status nutzen: `to-do`, `in-progress`, `review` oder `done` und einen der folgenden Werte für die Priority: `low`, `medium` oder `high`.
Request Body

{
"board": 12,
"title": "Code-Review durchführen",
"description": "Den neuen PR für das Feature X überprüfen",
"status": "review",
"priority": "medium",
"assignee_id": 13,
"reviewer_id": 1,
"due_date": "2025-02-27"
}

Success Response
Die Antwort enthält die erstellte Task mit allen zugehörigen Informationen.

{
"id": 10,
"board": 12,
"title": "Code-Review durchführen",
"description": "Den neuen PR für das Feature X überprüfen",
"status": "review",
"priority": "medium",
"assignee": {
"id": 13,
"email": "marie.musterfraun@example.com",
"fullname": "Marie Musterfrau"
},
"reviewer": {
"id": 1,
"email": "max.mustermann@example.com",
"fullname": "Max Mustermann"
},
"due_date": "2025-02-27",
"comments_count": 0
}

Status Codes

    201: Die Task wurde erfolgreich erstellt.
    400: Ungültige Anfragedaten. Möglicherweise fehlen erforderliche Felder oder enthalten ungültige Werte.
    401: Nicht autorisiert. Der Benutzer muss eingeloggt sein.
    403: Verboten. Der Benutzer muss Mitglied des Boards sein, um eine Task zu erstellen.
    404: Board nicht gefunden. Die angegebene Board-ID existiert nicht.
    500: Interner Serverfehler.

Rate Limits

    No limit

Permissions required: Der Benutzer muss Mitglied des Boards sein, um eine Task zu erstellen.
Extra Information: Sowohl `assignee` als auch `reviewer` müssen Mitglieder des Boards sein. Falls kein `assignee` oder `reviewer` angegeben wird, bleibt das Feld leer.

4.

PATCH
/api/tasks/{task_id}/
Description: Aktualisiert eine bestehende Task. Nur Mitglieder des Boards, zu dem die Task gehört, können sie bearbeiten.
URL Parameters
Name Type Description
task_id - Die ID der zu aktualisierenden Task.
Request Body

{
"title": "Code-Review abschließen",
"description": "Den PR fertig prüfen und Feedback geben",
"status": "done",
"priority": "high",
"assignee_id": 13,
"reviewer_id": 1,
"due_date": "2025-02-28"
}

Success Response
Die Antwort enthält die aktualisierte Task mit allen geänderten Werten.

{
"id": 10,
"title": "Code-Review abschließen",
"description": "Den PR fertig prüfen und Feedback geben",
"status": "done",
"priority": "high",
"assignee": {
"id": 13,
"email": "marie.musterfraun@example.com",
"fullname": "Marie Musterfrau"
},
"reviewer": {
"id": 1,
"email": "max.mustermann@example.com",
"fullname": "Max Mustermann"
},
"due_date": "2025-02-28"
}

Status Codes

    200: Die Task wurde erfolgreich aktualisiert.
    400: Ungültige Anfragedaten. Möglicherweise sind einige Werte ungültig oder nicht erlaubt.
    401: Nicht autorisiert. Der Benutzer muss eingeloggt sein.
    403: Verboten. Der Benutzer muss Mitglied des Boards sein, zu dem die Task gehört.
    404: Task nicht gefunden. Die angegebene Task-ID existiert nicht.
    500: Interner Serverfehler.

Rate Limits

    No limit

Permissions required: Der Benutzer muss Mitglied des Boards sein, um eine Task zu aktualisieren. Das ändern der Board-Id(board) ist nicht erlaubt!
Extra Information: Felder, die nicht aktualisiert werden sollen, können weggelassen werden. `assignee` und `reviewer` müssen weiterhin Mitglieder des Boards sein.

5.

DELETE
/api/tasks/{task_id}/
Description: Löscht eine bestehende Task. Nur der Ersteller der Task oder der Eigentümer des Boards kann die Task löschen.
URL Parameters
Name Type Description
task_id - Die ID der zu löschenden Task.
Request Body

{

}

Success Response
Wenn die Task erfolgreich gelöscht wurde, wird eine Bestätigung ohne Inhalt zurückgegeben.

null

Status Codes

    204: Die Task wurde erfolgreich gelöscht.
    400: Ungültige Anfragedaten. Die übermittelte Task-ID ist fehlerhaft.
    401: Nicht autorisiert. Der Benutzer muss eingeloggt sein.
    403: Verboten. Nur der Ersteller der Task oder der Board-Eigentümer kann die Task löschen.
    404: Task nicht gefunden. Die angegebene Task-ID existiert nicht.
    500: Interner Serverfehler.

Rate Limits

    No limit

Permissions required: Nur der Ersteller der Task oder der Eigentümer des Boards kann eine Task löschen.
Extra Information: Die Löschung ist dauerhaft und kann nicht rückgängig gemacht werden.

6.

GET
/api/tasks/{task_id}/comments/
Description: Ruft alle Kommentare ab, die einer bestimmten Task zugeordnet sind.
URL Parameters
Name Type Description
task_id - Die ID der Task, zu der die Kommentare abgerufen werden sollen.
Request Body

{

}

Success Response
Die Antwort enthält eine Liste aller Kommentare zur angegebenen Task. Jeder Kommentar enthält das Erstellungsdatum, den vollständigen Namen des Autors und den Inhalt.

[
{
"id": 1,
"created_at": "2025-02-20T14:30:00Z",
"author": "Max Mustermann",
"content": "Das ist ein Kommentar zur Task."
},
{
"id": 2,
"created_at": "2025-02-21T09:15:00Z",
"author": "Erika Musterfrau",
"content": "Ein weiterer Kommentar zur Diskussion."
}
]

Status Codes

    200: Erfolgreich. Gibt eine Liste der Kommentare zurück.
    401: Nicht autorisiert. Der Benutzer muss eingeloggt sein.
    403: Verboten. Der Benutzer muss Mitglied des Boards sein, zu dem die Task gehört.
    404: Task nicht gefunden. Die angegebene Task-ID existiert nicht.
    500: Interner Serverfehler.

Rate Limits

    No limit

Permissions required: Der Benutzer muss Mitglied des Boards sein, zu dem die Task gehört.
Extra Information: Die Kommentare sind chronologisch nach Erstellungsdatum sortiert.

7.

POST
/api/tasks/{task_id}/comments/
Description: Erstellt einen neuen Kommentar zu einer bestimmten Task. Der Autor wird automatisch anhand der Authentifizierung bestimmt.
URL Parameters
Name Type Description
task_id - Die ID der Task, zu der der Kommentar hinzugefügt werden soll.
Request Body

{
"content": "Das ist ein neuer Kommentar zur Task."
}

Success Response
Die Antwort enthält die erstellte Kommentarinstanz mit ID, Erstellungsdatum, vollständigem Namen des Autors und dem Inhalt.

{
"id": 15,
"created_at": "2025-02-20T15:00:00Z",
"author": "Max Mustermann",
"content": "Das ist ein neuer Kommentar zur Task."
}

Status Codes

    201: Der Kommentar wurde erfolgreich erstellt.
    400: Ungültige Anfragedaten. Möglicherweise ist der `content`-Wert leer.
    401: Nicht autorisiert. Der Benutzer muss eingeloggt sein.
    403: Verboten. Der Benutzer muss Mitglied des Boards sein, zu dem die Task gehört.
    404: Task nicht gefunden. Die angegebene Task-ID existiert nicht.
    500: Interner Serverfehler.

Rate Limits

    No limit

Permissions required: Der Benutzer muss Mitglied des Boards sein, zu dem die Task gehört.
Extra Information: Der Autor des Kommentars wird aus der Authentifizierung des aktuellen Benutzers bestimmt.

8.

DELETE
/api/tasks/{task_id}/comments/{comment_id}/
Description: Löscht einen Kommentar einer bestimmten Task. Nur der Ersteller des Kommentars kann ihn löschen.
URL Parameters
Name Type Description
task_id - Die ID der Task, zu der der Kommentar gehört.
comment_id - Die ID des zu löschenden Kommentars.
Request Body

{

}

Success Response
Bei erfolgreicher Löschung wird eine leere Antwort mit Statuscode `204` zurückgegeben.

null

Status Codes

    204: Der Kommentar wurde erfolgreich gelöscht.
    400: Ungültige Anfragedaten.
    401: Nicht autorisiert. Der Benutzer muss eingeloggt sein.
    403: Verboten. Nur der Ersteller des Kommentars darf ihn löschen.
    404: Kommentar oder Task nicht gefunden.
    500: Interner Serverfehler.

Rate Limits

    No limit

Permissions required: Nur der Benutzer, der den Kommentar erstellt hat, darf ihn löschen.
Extra Information: Falls der Kommentar oder die Task nicht existiert, wird ein `404`-Fehler zurückgegeben.
