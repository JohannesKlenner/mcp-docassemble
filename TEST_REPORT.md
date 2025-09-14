# MCP DOCASSEMBLE API TEST REPORT
Datum: 2025-09-14 20:08:36
Dauer: 81.6 Sekunden
Server: http://192.168.178.29

## ZUSAMMENFASSUNG
- ✅ Erfolgreich: 34/42 (81.0%)
- ❌ Fehlgeschlagen: 8/42

## DETAILLIERTE ERGEBNISSE

### Benutzer-Management
Erfolg: 12/12

- ✅ `create_user`: create_user funktioniert korrekt
- ✅ `invite_users`: invite_users funktioniert korrekt
- ✅ `list_users`: list_users funktioniert korrekt
- ✅ `get_user_by_username`: get_user_by_username funktioniert korrekt
- ✅ `get_current_user`: get_current_user funktioniert korrekt
- ✅ `update_current_user`: update_current_user funktioniert korrekt
- ✅ `get_user_by_id`: get_user_by_id funktioniert korrekt
- ✅ `deactivate_user`: deactivate_user funktioniert korrekt
- ✅ `update_user`: update_user funktioniert korrekt
- ✅ `list_privileges`: list_privileges funktioniert korrekt
- ✅ `give_user_privilege`: give_user_privilege funktioniert korrekt
- ✅ `remove_user_privilege`: remove_user_privilege funktioniert korrekt

### Interview-Management
Erfolg: 8/12

- ✅ `start_interview`: start_interview funktioniert korrekt
- ✅ `get_interview_variables`: get_interview_variables funktioniert korrekt
- ✅ `set_interview_variables`: set_interview_variables funktioniert korrekt
- ✅ `get_current_question`: get_current_question funktioniert korrekt
- ❌ `run_interview_action`: Unbekannter Fehler (501): API Request failed with status 501: 
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="mobile-web-app-capable" content="yes">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Error</title>
    <meta itemprop="name" content="docassemble: Error">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="docassemble: Error">
    <link rel="shortcut icon" href="/favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
    <link rel="icon" type="image/png" href="/favicon-32x32.png" sizes="32x32">
    <link rel="icon" type="image/png" href="/favicon-16x16.png" sizes="16x16">
    <link rel="manifest" href="/site.webmanifest">
    <link rel="mask-icon" href="/safari-pinned-tab.svg" color="#698aa7">
    <meta name="msapplication-TileColor" content="#da532c">
    <meta name="theme-color" content="#83b3dd">
    <script defer src="/static/fontawesome/js/all.min.js?v=1.8.13"></script>
    <link href="/static/bootstrap/css/bootstrap.min.css?v=1.8.13" rel="stylesheet">
    <link href="/static/app/app.min.css?v=1.8.13" rel="stylesheet">
  </head>
  <body class="dabody da-pad-for-navbar">
    <div class="danavbarcontainer" data-bs-theme="dark">
      <div class="navbar fixed-top navbar-expand-md bg-dark" role="banner">
        <div class="container danavcontainer justify-content-start">
          <a class="navbar-brand" href="#">Error</a>
          <button type="button" class="navbar-toggler ms-auto" data-bs-toggle="collapse" data-bs-target="#danavbar-collapse">
            <span class="navbar-toggler-icon"><span class="visually-hidden">Display the menu</span></span>
          </button>
          <div class="collapse navbar-collapse" id="danavbar-collapse">
            <ul class="navbar-nav ms-auto">
              <li class="nav-item dropdown show">
                <a href="#" id="navbarDropdown" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">admin@example.com</a>
                <div class="dropdown-menu dropdown-menu-right" aria-labelledby="navbarDropdown">
                  <a class="dropdown-item" href="/monitor">Monitor</a>
                  <a class="dropdown-item" href="/train">Train</a>
                  <a class="dropdown-item" href="/updatepackage">Package Management</a>
                  <a class="dropdown-item" href="/logs">Logs</a>
                  <a class="dropdown-item" href="/playground">Playground</a>
                  <a class="dropdown-item" href="/utilities">Utilities</a>
                  <a class="dropdown-item" href="/userlist">User List</a>
                  <a class="dropdown-item" href="/config">Configuration</a>
                  <a class="dropdown-item" href="/interviews">My Interviews</a>
                  <a class="dropdown-item" href="/user/profile">Profile</a>
                  <a class="dropdown-item" href="/user/sign-out">Sign Out</a>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    <div class="container" id="damain">
<h1>Error</h1>

<blockquote class="blockquote">KeyError: 'save_status'</blockquote>

<h3>Log</h3>

<pre>Traceback (most recent call last):
  File &#34;/usr/share/docassemble/local3.12/lib/python3.12/site-packages/docassemble/webapp/server.py&#34;, line 20970, in run_action_in_session
    interview.assemble(user_dict, interview_status)
  File &#34;/usr/share/docassemble/local3.12/lib/python3.12/site-packages/docassemble/base/parse.py&#34;, line 8741, in assemble
    user_dict[&#39;_internal&#39;][&#39;tracker&#39;] += 1
    ~~~~~~~~~^^^^^^^^^^^^^
TypeError: &#39;NoneType&#39; object is not subscriptable

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File &#34;/usr/share/docassemble/local3.12/lib/python3.12/site-packages/flask/app.py&#34;, line 917, in full_dispatch_request
    rv = self.dispatch_request()
         ^^^^^^^^^^^^^^^^^^^^^^^
  File &#34;/usr/share/docassemble/local3.12/lib/python3.12/site-packages/flask/app.py&#34;, line 902, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File &#34;/usr/share/docassemble/local3.12/lib/python3.12/site-packages/flask_cors/decorator.py&#34;, line 121, in wrapped_function
    resp = make_response(f(*args, **kwargs))
                         ^^^^^^^^^^^^^^^^^^
  File &#34;/usr/share/docassemble/local3.12/lib/python3.12/site-packages/docassemble/webapp/server.py&#34;, line 20905, in api_session_action
    result = run_action_in_session(**post_data)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File &#34;/usr/share/docassemble/local3.12/lib/python3.12/site-packages/docassemble/webapp/server.py&#34;, line 20993, in run_action_in_session
    if docassemble.base.functions.this_thread.misc[&#39;save_status&#39;] != SS_IGNORE:
       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
KeyError: &#39;save_status&#39;
</pre>


    </div>

    <script defer src="/static/app/adminbundle.min.js?v=1.8.13"></script>
    <script>
      var daAutoColorScheme = true;
      var daCurrentColorScheme = 0;
      var daUrlChangeColorScheme = "/color_scheme";
      var daRequestPath = "/api/session/action";
      var daButtonStyle = "btn-";
    </script>
    <script defer src="/static/app/501.min.js"></script>
    <script defer>Object.assign(window, {"daMessageLog": [], "daNotificationContainer": "<div class=\"datopcenter col-sm-7 col-md-6 col-lg-5\" id=\"daflash\"></div>", "daNotificationMessage": "<div class=\"da-alert alert alert-%s alert-dismissible fade show\" role=\"alert\">%s<button type=\"button\" class=\"btn-close\" data-bs-dismiss=\"alert\" aria-label=\"Close\"></button></div>"});</script>
  </body>
</html>
- ❌ `go_back_in_interview`: 400 - Ungültige Parameter: API Request failed with status 400: "Unable to obtain interview dictionary."

- ✅ `delete_interview_session`: delete_interview_session funktioniert korrekt
- ✅ `list_interview_sessions`: list_interview_sessions funktioniert korrekt
- ✅ `delete_interview_sessions`: delete_interview_sessions funktioniert korrekt
- ✅ `list_advertised_interviews`: list_advertised_interviews funktioniert korrekt
- ❌ `get_user_secret`: System-Fehler: DocassembleClient.get_user_secret() missing 2 required positional arguments: 'username' and 'password'
- ❌ `get_login_url`: System-Fehler: DocassembleClient.get_login_url() missing 2 required positional arguments: 'username' and 'password'

### Playground-Management
Erfolg: 4/6

- ✅ `list_playground_files`: list_playground_files funktioniert korrekt
- ✅ `delete_playground_file`: delete_playground_file funktioniert korrekt
- ✅ `list_playground_projects`: list_playground_projects funktioniert korrekt
- ❌ `create_playground_project`: 404 - Endpunkt nicht gefunden: API Request failed with status 404: <!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="mobile-web-app-capable" content="yes">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>404 Not Found</title>
    <meta itemprop="name" content="docassemble: Not Found">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="docassemble: Not Found">
    <link rel="shortcut icon" href="/favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
    <link rel="icon" type="image/png" href="/favicon-32x32.png" sizes="32x32">
    <link rel="icon" type="image/png" href="/favicon-16x16.png" sizes="16x16">
    <link rel="manifest" href="/site.webmanifest">
    <link rel="mask-icon" href="/safari-pinned-tab.svg" color="#698aa7">
    <meta name="msapplication-TileColor" content="#da532c">
    <meta name="theme-color" content="#83b3dd">
    <script defer src="/static/fontawesome/js/all.min.js?v=1.8.13"></script>
    <link href="/static/bootstrap/css/bootstrap.min.css?v=1.8.13" rel="stylesheet">
    <link href="/static/app/app.min.css?v=1.8.13" rel="stylesheet">
  </head>
  <body class="dabody da-pad-for-navbar">
    <div class="danavbarcontainer" data-bs-theme="dark">
      <div class="navbar fixed-top navbar-expand-md bg-dark" role="banner">
        <div class="container danavcontainer danavcontainer justify-content-start">
          <a class="navbar-brand" href="#">Not Found</a>
          <button type="button" class="navbar-toggler ms-auto" data-bs-toggle="collapse" data-bs-target="#danavbar-collapse">
            <span class="navbar-toggler-icon"><span class="visually-hidden">Display the menu</span></span>
          </button>
          <div class="collapse navbar-collapse" id="danavbar-collapse">
            <ul class="navbar-nav ms-auto">
            </ul>
          </div>
        </div>
      </div>
    </div>
    <div class="container" id="damain">
      <div class="row">
        <div class="offset-lg-3 col-lg-6 offset-md-2 col-md-8 offset-sm-1 col-sm-10">
          
<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>


        </div>
      </div>
    </div>

    <script defer src="/static/app/adminbundle.min.js?v=1.8.13"></script>
    <script>
      var daAutoColorScheme = true;
      var daCurrentColorScheme = 0;
      var daUrlChangeColorScheme = "/color_scheme";
      var daRequestPath = "/api/projects";
      var daButtonStyle = "btn-";
    </script>
  </body>
</html>
- ❌ `delete_playground_project`: 404 - Endpunkt nicht gefunden: API Request failed with status 404: <!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="mobile-web-app-capable" content="yes">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>404 Not Found</title>
    <meta itemprop="name" content="docassemble: Not Found">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="docassemble: Not Found">
    <link rel="shortcut icon" href="/favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
    <link rel="icon" type="image/png" href="/favicon-32x32.png" sizes="32x32">
    <link rel="icon" type="image/png" href="/favicon-16x16.png" sizes="16x16">
    <link rel="manifest" href="/site.webmanifest">
    <link rel="mask-icon" href="/safari-pinned-tab.svg" color="#698aa7">
    <meta name="msapplication-TileColor" content="#da532c">
    <meta name="theme-color" content="#83b3dd">
    <script defer src="/static/fontawesome/js/all.min.js?v=1.8.13"></script>
    <link href="/static/bootstrap/css/bootstrap.min.css?v=1.8.13" rel="stylesheet">
    <link href="/static/app/app.min.css?v=1.8.13" rel="stylesheet">
  </head>
  <body class="dabody da-pad-for-navbar">
    <div class="danavbarcontainer" data-bs-theme="dark">
      <div class="navbar fixed-top navbar-expand-md bg-dark" role="banner">
        <div class="container danavcontainer danavcontainer justify-content-start">
          <a class="navbar-brand" href="#">Not Found</a>
          <button type="button" class="navbar-toggler ms-auto" data-bs-toggle="collapse" data-bs-target="#danavbar-collapse">
            <span class="navbar-toggler-icon"><span class="visually-hidden">Display the menu</span></span>
          </button>
          <div class="collapse navbar-collapse" id="danavbar-collapse">
            <ul class="navbar-nav ms-auto">
            </ul>
          </div>
        </div>
      </div>
    </div>
    <div class="container" id="damain">
      <div class="row">
        <div class="offset-lg-3 col-lg-6 offset-md-2 col-md-8 offset-sm-1 col-sm-10">
          
<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>


        </div>
      </div>
    </div>

    <script defer src="/static/app/adminbundle.min.js?v=1.8.13"></script>
    <script>
      var daAutoColorScheme = true;
      var daCurrentColorScheme = 0;
      var daUrlChangeColorScheme = "/color_scheme";
      var daRequestPath = "/api/projects";
      var daButtonStyle = "btn-";
    </script>
  </body>
</html>
- ✅ `clear_interview_cache`: clear_interview_cache funktioniert korrekt

### Server-Management
Erfolg: 6/7

- ✅ `get_server_config`: get_server_config funktioniert korrekt
- ✅ `list_installed_packages`: list_installed_packages funktioniert korrekt
- ✅ `install_package`: install_package funktioniert korrekt
- ❌ `uninstall_package`: 400 - Ungültige Parameter: API Request failed with status 400: "Package not found."

- ✅ `get_package_update_status`: get_package_update_status funktioniert korrekt
- ✅ `trigger_server_restart`: trigger_server_restart funktioniert korrekt
- ✅ `get_restart_status`: get_restart_status funktioniert korrekt

### Daten & API-Keys
Erfolg: 4/5

- ✅ `get_user_api_keys`: get_user_api_keys funktioniert korrekt
- ✅ `create_user_api_key`: create_user_api_key funktioniert korrekt
- ✅ `delete_user_api_key`: delete_user_api_key funktioniert korrekt
- ✅ `get_interview_data`: get_interview_data funktioniert korrekt
- ❌ `retrieve_stashed_data`: 400 - Ungültige Parameter: API Request failed with status 400: "The stashed data could not be retrieved: AssertionError ."


