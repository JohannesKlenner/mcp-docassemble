# OFFIZIELLE DOCASSEMBLE API ENDPUNKTE
## Extrahiert aus https://docassemble.org/docs/api.html am 14. September 2025

### BENUTZER-MANAGEMENT (15 Endpunkte)
1. **Create a new user** - `POST /api/user/new`
2. **Invite a new user** - `POST /api/user_invite`
3. **List of users** - `GET /api/user_list`
4. **Retrieve user information by username** - `GET /api/user_info`
5. **Retrieve information about the user** - `GET /api/user`
6. **Set information about the user** - `PATCH /api/user`
7. **Information about a given user** - `GET /api/user/<user_id>`
8. **Make a user inactive** - `DELETE /api/user/<user_id>`
9. **Set information about a user** - `PATCH /api/user/<user_id>`
10. **List available privileges** - `GET /api/privileges`
11. **Add a role to the list of available privileges** - `POST /api/privileges`
12. **Give a user a privilege** - `POST /api/user/<user_id>/privileges`
13. **Take a privilege away from a user** - `DELETE /api/user/<user_id>/privileges`
14. **Get information about the user's API keys** - `GET /api/user/api`
15. **Delete an API key belonging to the user** - `DELETE /api/user/api`
16. **Add a new API key for the user** - `POST /api/user/api`
17. **Update an API key for the user** - `PATCH /api/user/api`
18. **Get information about a given user's API keys** - `GET /api/user/<user_id>/api`
19. **Delete an API key belonging to a given user** - `DELETE /api/user/<user_id>/api`
20. **Add a new API key for a given user** - `POST /api/user/<user_id>/api`
21. **Update an API key for a given user** - `PATCH /api/user/<user_id>/api`

### INTERVIEW-MANAGEMENT (17 Endpunkte)
22. **List interview sessions on the system** - `GET /api/interviews`
23. **Delete interview sessions on the system** - `DELETE /api/interviews`
24. **List interview sessions of the user** - `GET /api/user/interviews`
25. **Delete interview sessions of the user** - `DELETE /api/user/interviews`
26. **List interview sessions of another user** - `GET /api/user/<user_id>/interviews`
27. **Delete interview sessions of another user** - `DELETE /api/user/<user_id>/interviews`
28. **Create new session** - `GET /api/session/new`
29. **Get answers from a session** - `GET /api/session`
30. **Send variables to a session** - `POST /api/session`
31. **Send variables to a session (logged-in user)** - `POST /api/user/interviews/session`
32. **Delete an interview session** - `DELETE /api/session`
33. **Get the current question in an interview** - `GET /api/session/question`
34. **Run an action in an interview** - `POST /api/session/action`
35. **Go back in an interview** - `POST /api/session/back`
36. **Create a temporary URL for launching an interview** - `GET /api/temp_url`
37. **Get the secret of a user** - `GET /api/secret`
38. **Get a login URL for a user** - `GET /api/login_url`

### PLAYGROUND-MANAGEMENT (7 Endpunkte)
39. **List the contents of the Playground** - `GET /api/playground`
40. **Update or create a file in the Playground** - `POST /api/playground`
41. **Delete a file in the Playground** - `DELETE /api/playground`
42. **Clear the interview cache** - `POST /api/clear_cache`
43. **Get the list of projects in the Playground** - `GET /api/projects`
44. **Create a project in the Playground** - `POST /api/projects`
45. **Delete a project in the Playground** - `DELETE /api/projects`

### SERVER-MANAGEMENT (9 Endpunkte)
46. **Get the server configuration** - `GET /api/config`
47. **Write the server configuration** - `POST /api/config`
48. **Update the server configuration** - `PATCH /api/config`
49. **List the packages installed** - `GET /api/package`
50. **Install or update a package** - `POST /api/package`
51. **Uninstall a package** - `DELETE /api/package`
52. **Poll the status of a package update process** - `GET /api/package_update_status`
53. **Trigger a server restart** - `POST /api/restart`
54. **Poll the status of a restart** - `GET /api/restart_status`

### DATEN & DATEIEN (6 Endpunkte)
55. **Get list of available interviews** - `GET /api/list`
56. **Get information about fields in PDF/DOCX template** - `POST /api/fields`
57. **Convert a file to Markdown** - `POST /api/convert_file`
58. **Obtain information about an interview** - `GET /api/interview_data`
59. **Temporarily stash encrypted data** - `POST /api/stash_data`
60. **Retrieve temporarily stashed data** - `GET /api/retrieve_stashed_data`

## GESAMT: 60 OFFIZIELLE API-ENDPUNKTE
