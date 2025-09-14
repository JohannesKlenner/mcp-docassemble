"""
Docassemble API Client

Vollständige Implementierung aller 61 Docassemble API Endpunkte
Enhanced with version detection, graceful fallbacks, and improved error handling.
"""

import json
import logging
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin

import requests
from pydantic import BaseModel, Field

from .enhancements import DocassembleClientEnhanced


logger = logging.getLogger(__name__)


class DocassembleAPIError(Exception):
    """Docassemble API Fehler"""
    def __init__(self, message: str, status_code: Optional[int] = None, response_data: Optional[str] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class DocassembleClient(DocassembleClientEnhanced):
    """
    Vollständiger Docassemble API Client mit allen 61 verfügbaren Endpunkten.
    Enhanced with version detection, graceful fallbacks, and improved session management.
    
    Authentifizierung erfolgt über API-Schlüssel im X-API-Key Header oder als Bearer Token.
    Alle Endpunkte sind nach Kategorien organisiert.
    """
    
    __version__ = "1.1.0"
    
    def __init__(self, base_url: str, api_key: str, timeout: int = 30, 
                 session_timeout: int = 3600, enable_fallbacks: bool = True):
        """
        Initialisiere Docassemble Client
        
        Args:
            base_url: Base URL des Docassemble Servers (z.B. https://docassemble.example.com)
            api_key: API Schlüssel für Authentifizierung
            timeout: Request timeout in seconds (default: 30)
            session_timeout: Interview session timeout in seconds (default: 3600)
            enable_fallbacks: Enable graceful fallbacks for unsupported APIs (default: True)
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.session_timeout = session_timeout
        self.enable_fallbacks = enable_fallbacks
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': api_key,
            'Content-Type': 'application/json'
        })
        
        # Detect Docassemble version and capabilities
        self.da_version = self._detect_docassemble_version()
        self._init_feature_compatibility()
    
    def _detect_docassemble_version(self) -> Optional[str]:
        """Detect Docassemble version and capabilities."""
        try:
            response = self.session.get(f"{self.base_url}/api/config", timeout=self.timeout)
            if response.status_code == 200:
                config = response.json()
                version = config.get('version', 'unknown')
                logger.info(f"Detected Docassemble version: {version}")
                return version
        except Exception as e:
            logger.warning(f"Could not detect Docassemble version: {e}")
        return None
    
    def _init_feature_compatibility(self):
        """Initialize feature compatibility matrix based on version."""
        self.feature_support = {
            'convert_file_to_markdown': False,  # Not available in current versions
            'get_redirect_url': False,          # Now using correct /api/temp_url endpoint  
            'get_login_url': False,             # Limited availability
            'pull_package_to_playground': False, # Version dependent
            'advanced_session_management': True,  # Available but needs proper handling
        }
        
        # Adjust based on detected version
        if self.da_version and 'dev' in self.da_version.lower():
            # Development versions might have more features
            self.feature_support.update({
                'convert_file_to_markdown': True,
                'get_redirect_url': True,
            })
    
    def _is_feature_supported(self, feature: str) -> bool:
        """Check if a feature is supported in current version."""
        return self.feature_support.get(feature, True)
    
    def _graceful_fallback(self, feature_name: str, fallback_result: Any = None):
        """Provide graceful fallback for unsupported features."""
        if not self.enable_fallbacks:
            raise DocassembleAPIError(f"Feature '{feature_name}' not supported in this Docassemble version")
        
        logger.warning(f"Feature '{feature_name}' not available, using fallback")
        return fallback_result or {"status": "unsupported", "feature": feature_name, "message": "Feature not available in this version"}
    
    def _request(self, method: str, endpoint: str, params: Optional[Dict] = None, 
                data: Optional[Dict] = None, files: Optional[Dict] = None) -> Any:
        """
        Führt HTTP Request aus
        
        Args:
            method: HTTP Methode (GET, POST, DELETE, PATCH)
            endpoint: API Endpunkt Pfad
            params: URL Parameter
            data: Request Body Daten
            files: Datei-Uploads
            
        Returns:
            Response Daten als JSON oder None für leere Responses
            
        Raises:
            DocassembleAPIError: Bei API Fehlern
        """
        url = urljoin(self.base_url + '/', endpoint.lstrip('/'))
        
        kwargs = {}
        if params:
            kwargs['params'] = params
        if data and not files:
            kwargs['json'] = data
        elif data and files:
            kwargs['data'] = data
            kwargs['files'] = files
            # Entferne Content-Type Header für multipart/form-data
            headers = self.session.headers.copy()
            headers.pop('Content-Type', None)
            kwargs['headers'] = headers
        elif files:
            kwargs['files'] = files
            headers = self.session.headers.copy()
            headers.pop('Content-Type', None)
            kwargs['headers'] = headers
            
        try:
            response = self.session.request(method, url, **kwargs)
            
            # Erfolgreiche leere Responses
            if response.status_code in [204]:
                return None
                
            # Erfolgreiche Responses mit Content
            if 200 <= response.status_code < 300:
                if response.headers.get('content-type', '').startswith('application/json'):
                    return response.json()
                else:
                    return response.text
                    
            # Fehler Responses
            error_msg = f"API Request failed with status {response.status_code}"
            if response.text:
                error_msg += f": {response.text}"
                
            raise DocassembleAPIError(
                error_msg, 
                status_code=response.status_code,
                response_data=response.text
            )
            
        except requests.RequestException as e:
            raise DocassembleAPIError(f"Request failed: {str(e)}")

    # ====================================================================
    # BENUTZER-MANAGEMENT (9 Endpunkte)
    # ====================================================================
    
    def create_user(self, username: str, password: Optional[str] = None, 
                   privileges: Optional[List[str]] = None, first_name: Optional[str] = None,
                   last_name: Optional[str] = None, country: Optional[str] = None,
                   subdivisionfirst: Optional[str] = None, subdivisionsecond: Optional[str] = None,
                   subdivisionthird: Optional[str] = None, organization: Optional[str] = None,
                   timezone: Optional[str] = None, language: Optional[str] = None) -> Dict[str, Any]:
        """
        Erstellt einen neuen Benutzer
        
        Benötigte Berechtigungen: admin oder (access_user_info und create_user)
        
        Args:
            username: Benutzername (E-Mail Adresse)
            password: Passwort (optional, wird automatisch generiert wenn nicht angegeben)
            privileges: Liste der Benutzerrechte (optional, default: ['user'])
            first_name: Vorname (optional)
            last_name: Nachname (optional)
            country: Ländercode (optional, z.B. 'US')
            subdivisionfirst: Bundesland/Staat (optional)
            subdivisionsecond: Landkreis (optional)
            subdivisionthird: Gemeinde (optional)
            organization: Organisation (optional)
            timezone: Zeitzone (optional, z.B. 'America/New_York')
            language: Sprachcode (optional, z.B. 'en')
            
        Returns:
            Dict mit user_id und password des neuen Benutzers
        """
        data = {'username': username}
        if password:
            data['password'] = password
        if privileges:
            data['privileges'] = privileges
        if first_name:
            data['first_name'] = first_name
        if last_name:
            data['last_name'] = last_name
        if country:
            data['country'] = country
        if subdivisionfirst:
            data['subdivisionfirst'] = subdivisionfirst
        if subdivisionsecond:
            data['subdivisionsecond'] = subdivisionsecond
        if subdivisionthird:
            data['subdivisionthird'] = subdivisionthird
        if organization:
            data['organization'] = organization
        if timezone:
            data['timezone'] = timezone
        if language:
            data['language'] = language
            
        return self._request('POST', '/api/user/new', data=data)
    
    def invite_users(self, email_addresses: List[str], privilege: Optional[str] = None,
                    send_emails: bool = True) -> List[Dict[str, Any]]:
        """
        Lädt neue Benutzer per E-Mail ein
        
        Benötigte Berechtigungen: admin oder create_user
        
        Args:
            email_addresses: Liste der E-Mail Adressen
            privilege: Einzelnes Benutzerrecht (optional, default: 'user')
            send_emails: Ob E-Mail Einladungen gesendet werden sollen
            
        Returns:
            Liste mit Einladungsdetails für jede E-Mail
        """
        data = {'email_addresses': email_addresses}
        if privilege:
            data['privilege'] = privilege
        if not send_emails:
            data['send_emails'] = '0'
            
        return self._request('POST', '/api/user_invite', data=data)
    
    def list_users(self, include_inactive: bool = False, next_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Listet alle registrierten Benutzer (paginiert)
        
        Benötigte Berechtigungen: admin, advocate oder access_user_info
        
        Args:
            include_inactive: Ob inaktive Benutzer eingeschlossen werden sollen
            next_id: ID für nächste Seite der Ergebnisse
            
        Returns:
            Dict mit 'items' (Benutzerliste) und 'next_id' für Pagination
        """
        params = {}
        if include_inactive:
            params['include_inactive'] = '1'
        if next_id:
            params['next_id'] = next_id
            
        return self._request('GET', '/api/user_list', params=params)
    
    def get_user_by_username(self, username: str) -> Dict[str, Any]:
        """
        Holt Benutzerinformationen per Benutzername
        
        Benötigte Berechtigungen: admin, advocate oder access_user_info
        
        Args:
            username: Benutzername (E-Mail Adresse)
            
        Returns:
            Benutzerinformationen
        """
        return self._request('GET', '/api/user_info', params={'username': username})
    
    def get_current_user(self) -> Dict[str, Any]:
        """
        Holt Informationen über den aktuellen Benutzer (API Key Besitzer)
        
        Benötigte Berechtigungen: Keine
        
        Returns:
            Benutzerinformationen des API Key Besitzers
        """
        return self._request('GET', '/api/user')
    
    def update_current_user(self, first_name: Optional[str] = None, last_name: Optional[str] = None,
                           country: Optional[str] = None, subdivisionfirst: Optional[str] = None,
                           subdivisionsecond: Optional[str] = None, subdivisionthird: Optional[str] = None,
                           organization: Optional[str] = None, timezone: Optional[str] = None,
                           language: Optional[str] = None, password: Optional[str] = None,
                           old_password: Optional[str] = None) -> None:
        """
        Aktualisiert Informationen des aktuellen Benutzers
        
        Benötigte Berechtigungen: edit_user_info für Profildaten, edit_user_password für Passwort
        
        Args:
            first_name: Neuer Vorname
            last_name: Neuer Nachname
            country: Neuer Ländercode
            subdivisionfirst: Neues Bundesland/Staat
            subdivisionsecond: Neuer Landkreis
            subdivisionthird: Neue Gemeinde
            organization: Neue Organisation
            timezone: Neue Zeitzone
            language: Neue Sprache
            password: Neues Passwort
            old_password: Altes Passwort (für Verschlüsselungskonvertierung)
        """
        data = {}
        if first_name:
            data['first_name'] = first_name
        if last_name:
            data['last_name'] = last_name
        if country:
            data['country'] = country
        if subdivisionfirst:
            data['subdivisionfirst'] = subdivisionfirst
        if subdivisionsecond:
            data['subdivisionsecond'] = subdivisionsecond
        if subdivisionthird:
            data['subdivisionthird'] = subdivisionthird
        if organization:
            data['organization'] = organization
        if timezone:
            data['timezone'] = timezone
        if language:
            data['language'] = language
        if password:
            data['password'] = password
        if old_password:
            data['old_password'] = old_password
            
        return self._request('PATCH', '/api/user', data=data)
    
    def get_user_by_id(self, user_id: int) -> Dict[str, Any]:
        """
        Holt Informationen über einen Benutzer per ID
        
        Benötigte Berechtigungen: admin, advocate, eigene ID oder access_user_info
        
        Args:
            user_id: Benutzer ID
            
        Returns:
            Benutzerinformationen
        """
        return self._request('GET', f'/api/user/{user_id}')
    
    def deactivate_user(self, user_id: int, remove: Optional[str] = None) -> None:
        """
        Deaktiviert oder löscht einen Benutzer
        
        Benötigte Berechtigungen: admin oder (access_user_info und edit_user_active_status/delete_user)
        
        Args:
            user_id: Benutzer ID
            remove: 'account' zum Löschen, 'account_and_shared' für vollständiges Löschen
        """
        params = {}
        if remove:
            params['remove'] = remove
            
        return self._request('DELETE', f'/api/user/{user_id}', params=params)
    
    def update_user(self, user_id: int, country: Optional[str] = None, first_name: Optional[str] = None,
                   language: Optional[str] = None, last_name: Optional[str] = None,
                   organization: Optional[str] = None, subdivisionfirst: Optional[str] = None,
                   subdivisionsecond: Optional[str] = None, subdivisionthird: Optional[str] = None,
                   timezone: Optional[str] = None, password: Optional[str] = None,
                   old_password: Optional[str] = None, active: Optional[bool] = None) -> None:
        """
        Aktualisiert Informationen eines Benutzers
        
        Benötigte Berechtigungen: admin oder entsprechende Permissions
        
        Args:
            user_id: Benutzer ID
            country: Ländercode
            first_name: Vorname
            language: Sprachcode
            last_name: Nachname
            organization: Organisation
            subdivisionfirst: Bundesland/Staat
            subdivisionsecond: Landkreis
            subdivisionthird: Gemeinde
            timezone: Zeitzone
            password: Neues Passwort
            old_password: Altes Passwort
            active: Aktiv-Status
        """
        data = {}
        if country:
            data['country'] = country
        if first_name:
            data['first_name'] = first_name
        if language:
            data['language'] = language
        if last_name:
            data['last_name'] = last_name
        if organization:
            data['organization'] = organization
        if subdivisionfirst:
            data['subdivisionfirst'] = subdivisionfirst
        if subdivisionsecond:
            data['subdivisionsecond'] = subdivisionsecond
        if subdivisionthird:
            data['subdivisionthird'] = subdivisionthird
        if timezone:
            data['timezone'] = timezone
        if password:
            data['password'] = password
        if old_password:
            data['old_password'] = old_password
        if active is not None:
            data['active'] = active
            
        return self._request('PATCH', f'/api/user/{user_id}', data=data)

    # ====================================================================
    # BERECHTIGUNGEN (4 Endpunkte)
    # ====================================================================
    
    def list_privileges(self) -> List[str]:
        """
        Listet alle verfügbaren Berechtigungen im System
        
        Benötigte Berechtigungen: admin, developer oder access_privileges
        
        Returns:
            Liste der verfügbaren Berechtigungsnamen
        """
        return self._request('GET', '/api/privileges')
    
    def add_privilege_to_role(self, privilege_name: str) -> None:
        """
        Fügt eine neue Berechtigung zur Liste der verfügbaren Berechtigungen hinzu
        
        Benötigte Berechtigungen: admin oder access_privileges und edit_privileges
        
        Args:
            privilege_name: Name der neuen Berechtigung
        """
        return self._request('POST', '/api/privileges', data={'privilege': privilege_name})
    
    def give_user_privilege(self, user_id: int, privilege: str) -> None:
        """
        Gibt einem Benutzer eine Berechtigung
        
        Benötigte Berechtigungen: admin oder (access_privileges und edit_user_privileges)
        
        Args:
            user_id: Benutzer ID
            privilege: Name der Berechtigung
        """
        return self._request('POST', f'/api/user/{user_id}/privileges', data={'privilege': privilege})
    
    def remove_user_privilege(self, user_id: int, privilege: str) -> None:
        """
        Entzieht einem Benutzer eine Berechtigung
        
        Benötigte Berechtigungen: admin oder edit_user_privileges
        
        Args:
            user_id: Benutzer ID
            privilege: Name der Berechtigung
        """
        return self._request('DELETE', f'/api/user/{user_id}/privileges', params={'privilege': privilege})

    # ====================================================================
    # INTERVIEW SESSIONS (12 Endpunkte)  
    # ====================================================================
    
    def list_interview_sessions(self, secret: Optional[str] = None, i: Optional[str] = None,
                               session: Optional[str] = None, query: Optional[str] = None,
                               tag: Optional[str] = None, include_dictionary: bool = False,
                               next_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Listet Interview Sessions im System (paginiert)
        
        Benötigte Berechtigungen: admin, advocate oder access_sessions
        
        Args:
            secret: Entschlüsselungskey für verschlüsselte Sessions
            i: Interview Dateiname Filter
            session: Session ID Filter
            query: Session Query String Filter
            tag: Tag Filter
            include_dictionary: Ob Interview Antworten eingeschlossen werden sollen
            next_id: ID für nächste Seite
            
        Returns:
            Dict mit 'items' (Session Liste) und 'next_id'
        """
        params = {}
        if secret:
            params['secret'] = secret
        if i:
            params['i'] = i
        if session:
            params['session'] = session
        if query:
            params['query'] = query
        if tag:
            params['tag'] = tag
        if include_dictionary:
            params['include_dictionary'] = '1'
        if next_id:
            params['next_id'] = next_id
            
        return self._request('GET', '/api/interviews', params=params)
    
    def delete_interview_sessions(self, i: Optional[str] = None, session: Optional[str] = None,
                                 query: Optional[str] = None, tag: Optional[str] = None) -> None:
        """
        Löscht Interview Sessions im System
        
        Benötigte Berechtigungen: admin oder (access_sessions und edit_sessions)
        
        Args:
            i: Interview Dateiname Filter
            session: Session ID Filter
            query: Session Query String Filter
            tag: Tag Filter
        """
        params = {}
        if i:
            params['i'] = i
        if session:
            params['session'] = session
        if query:
            params['query'] = query
        if tag:
            params['tag'] = tag
            
        return self._request('DELETE', '/api/interviews', params=params)
    
    def list_user_interview_sessions(self, secret: Optional[str] = None, i: Optional[str] = None,
                                    session: Optional[str] = None, query: Optional[str] = None,
                                    tag: Optional[str] = None, include_dictionary: bool = False,
                                    next_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Listet Interview Sessions des aktuellen Benutzers
        
        Benötigte Berechtigungen: access_sessions (bei beschränkten Permissions)
        
        Args:
            secret: Entschlüsselungskey
            i: Interview Dateiname Filter
            session: Session ID Filter
            query: Session Query String Filter
            tag: Tag Filter
            include_dictionary: Ob Interview Antworten eingeschlossen werden sollen
            next_id: ID für nächste Seite
            
        Returns:
            Dict mit Sessions des aktuellen Benutzers
        """
        params = {}
        if secret:
            params['secret'] = secret
        if i:
            params['i'] = i
        if session:
            params['session'] = session
        if query:
            params['query'] = query
        if tag:
            params['tag'] = tag
        if include_dictionary:
            params['include_dictionary'] = '1'
        if next_id:
            params['next_id'] = next_id
            
        return self._request('GET', '/api/user/interviews', params=params)
    
    def delete_user_interview_sessions(self, i: Optional[str] = None, session: Optional[str] = None,
                                      query: Optional[str] = None, tag: Optional[str] = None) -> None:
        """
        Löscht Interview Sessions des aktuellen Benutzers
        
        Benötigte Berechtigungen: access_sessions und edit_sessions (bei beschränkten Permissions)
        
        Args:
            i: Interview Dateiname Filter
            session: Session ID Filter
            query: Session Query String Filter
            tag: Tag Filter
        """
        params = {}
        if i:
            params['i'] = i
        if session:
            params['session'] = session
        if query:
            params['query'] = query
        if tag:
            params['tag'] = tag
            
        return self._request('DELETE', '/api/user/interviews', params=params)
    
    def list_user_sessions_by_id(self, user_id: int, i: Optional[str] = None,
                                session: Optional[str] = None, query: Optional[str] = None,
                                tag: Optional[str] = None, next_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Listet Interview Sessions eines bestimmten Benutzers
        
        Benötigte Berechtigungen: admin, advocate, eigene ID oder access_sessions
        
        Args:
            user_id: Benutzer ID
            i: Interview Dateiname Filter
            session: Session ID Filter
            query: Session Query String Filter
            tag: Tag Filter
            next_id: ID für nächste Seite
            
        Returns:
            Dict mit Sessions des angegebenen Benutzers
        """
        params = {}
        if i:
            params['i'] = i
        if session:
            params['session'] = session
        if query:
            params['query'] = query
        if tag:
            params['tag'] = tag
        if next_id:
            params['next_id'] = next_id
            
        return self._request('GET', f'/api/user/{user_id}/interviews', params=params)
    
    def delete_user_sessions_by_id(self, user_id: int, i: Optional[str] = None,
                                  session: Optional[str] = None, query: Optional[str] = None,
                                  tag: Optional[str] = None) -> None:
        """
        Löscht Interview Sessions eines bestimmten Benutzers
        
        Benötigte Berechtigungen: admin, advocate, eigene ID oder edit_sessions
        
        Args:
            user_id: Benutzer ID
            i: Interview Dateiname Filter
            session: Session ID Filter
            query: Session Query String Filter
            tag: Tag Filter
        """
        params = {}
        if i:
            params['i'] = i
        if session:
            params['session'] = session
        if query:
            params['query'] = query
        if tag:
            params['tag'] = tag
            
        return self._request('DELETE', f'/api/user/{user_id}/interviews', params=params)
    
    def list_advertised_interviews(self, tag: Optional[str] = None, absolute_urls: bool = True) -> List[Dict[str, Any]]:
        """
        Holt Liste der beworbenen Interviews
        
        Benötigte Berechtigungen: Keine
        
        Args:
            tag: Tag Filter für Interviews
            absolute_urls: Ob absolute URLs zurückgegeben werden sollen
            
        Returns:
            Liste der verfügbaren Interviews
        """
        params = {}
        if tag:
            params['tag'] = tag
        if not absolute_urls:
            params['absolute_urls'] = '0'
            
        return self._request('GET', '/api/list', params=params)
    
    def get_user_secret(self, username: str, password: str) -> str:
        """
        Holt Entschlüsselungskey für einen Benutzer
        
        Benötigte Berechtigungen: Keine
        
        Args:
            username: Benutzername
            password: Passwort
            
        Returns:
            Entschlüsselungskey als String
        """
        params = {'username': username, 'password': password}
        return self._request('GET', '/api/secret', params=params)
    
    def get_login_url(self, username: str, password: str, i: Optional[str] = None,
                     session: Optional[str] = None, resume_existing: bool = False,
                     expire: int = 15, url_args: Optional[Dict] = None,
                     next: Optional[str] = None) -> str:
        """
        Erstellt temporäre Login URL für einen Benutzer
        
        Benötigte Berechtigungen: admin oder log_user_in
        
        Args:
            username: Benutzername
            password: Passwort
            i: Interview Dateiname (optional)
            session: Session ID (optional)
            resume_existing: Ob existierende Session fortgesetzt werden soll
            expire: Ablaufzeit in Sekunden (default: 15)
            url_args: Zusätzliche URL Parameter
            next: Seite nach Login (statt Interview)
            
        Returns:
            Temporäre Login URL
        """
        data = {'username': username, 'password': password}
        if i:
            data['i'] = i
        if session:
            data['session'] = session
        if resume_existing:
            data['resume_existing'] = '1'
        if expire != 15:
            data['expire'] = expire
        if url_args:
            data['url_args'] = url_args
        if next:
            data['next'] = next
            
        return self._request('POST', '/api/login_url', data=data)
    
    def get_resume_url(self, i: str, session: str, expire: int = 15,
                      url_args: Optional[Dict] = None) -> str:
        """
        Erstellt URL zum Fortsetzen einer existierenden Session
        
        Benötigte Berechtigungen: Keine
        
        Args:
            i: Interview Dateiname
            session: Session ID
            expire: Ablaufzeit in Sekunden
            url_args: Zusätzliche URL Parameter
            
        Returns:
            Temporäre Resume URL
        """
        data = {'i': i, 'session': session}
        if expire != 15:
            data['expire'] = expire
        if url_args:
            data['url_args'] = url_args
            
        return self._request('POST', '/api/resume_url', data=data)
    
    def get_redirect_url(self, url: str, expire: int = 3600, one_time: bool = False) -> str:
        """
        Erstellt allgemeine Redirect URL (Official API: /api/temp_url)
        
        Benötigte Berechtigungen: Keine
        
        Args:
            url: Ziel URL
            expire: Ablaufzeit in Sekunden (default: 3600)
            one_time: URL verfällt nach einmaliger Nutzung
            
        Returns:
            Temporäre Redirect URL
        """
        params = {'url': url}
        if expire != 3600:
            params['expire'] = expire
        if one_time:
            params['one_time'] = 1
            
        return self._request('GET', '/api/temp_url', params=params)

    # ====================================================================
    # INTERVIEW OPERATIONS (8 Endpunkte)
    # ====================================================================
    
    def start_interview(self, i: str, secret: Optional[str] = None, **url_args) -> Dict[str, Any]:
        """
        Startet eine neue Interview Session
        
        Benötigte Berechtigungen: Keine (abhängig vom Interview)
        
        Args:
            i: Interview Dateiname (z.B. 'docassemble.demo:data/questions/questions.yml')
            secret: Verschlüsselungskey (optional)
            **url_args: Zusätzliche Parameter werden als url_args übergeben
            
        Returns:
            Dict mit session ID, encrypted Status und optional secret
        """
        params = {'i': i}
        if secret:
            params['secret'] = secret
        params.update(url_args)
        
        return self._request('GET', '/api/session/new', params=params)
    
    def get_interview_variables(self, i: str, session: str, secret: Optional[str] = None) -> Dict[str, Any]:
        """
        Holt alle Variablen aus einer Interview Session
        
        Benötigte Berechtigungen: Keine
        
        Args:
            i: Interview Dateiname
            session: Session ID
            secret: Entschlüsselungskey (falls verschlüsselt)
            
        Returns:
            JSON Repräsentation des Interview Dictionary
        """
        params = {'i': i, 'session': session}
        if secret:
            params['secret'] = secret
            
        return self._request('GET', '/api/session', params=params)
    
    def set_interview_variables(self, i: str, session: str, secret: Optional[str] = None,
                               variables: Optional[Dict] = None, raw: bool = False,
                               question_name: Optional[str] = None, question: bool = True,
                               delete_variables: Optional[List[str]] = None,
                               event_list: Optional[List] = None,
                               file_variables: Optional[Dict] = None,
                               files: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
        """
        Setzt Variablen in einer Interview Session
        
        Benötigte Berechtigungen: Keine
        
        Args:
            i: Interview Dateiname
            session: Session ID
            secret: Entschlüsselungskey (falls verschlüsselt)
            variables: Dict mit Variablen und Werten
            raw: Ob Datum/Objekt Konvertierung übersprungen werden soll
            question_name: Name der beantworteten Frage
            question: Ob Interview nach Setzen evaluiert werden soll
            delete_variables: Liste zu löschender Variablen
            event_list: Event Liste
            file_variables: Datei-Variablen
            files: Datei-Uploads
            
        Returns:
            JSON der aktuellen Frage oder None wenn question=False
        """
        data = {'i': i, 'session': session}
        if secret:
            data['secret'] = secret
        if variables:
            data['variables'] = variables
        if raw:
            data['raw'] = '0'
        if question_name:
            data['question_name'] = question_name
        if not question:
            data['question'] = '0'
        if delete_variables:
            data['delete_variables'] = delete_variables
        if event_list:
            data['event_list'] = event_list
        if file_variables:
            data['file_variables'] = file_variables
            
        return self._request('POST', '/api/session', data=data, files=files)
    
    def get_current_question(self, i: str, session: str, secret: Optional[str] = None) -> Dict[str, Any]:
        """
        Holt Informationen über die aktuelle Frage
        
        Benötigte Berechtigungen: Keine
        
        Args:
            i: Interview Dateiname
            session: Session ID
            secret: Entschlüsselungskey (falls verschlüsselt)
            
        Returns:
            JSON Repräsentation der aktuellen Frage
        """
        params = {'i': i, 'session': session}
        if secret:
            params['secret'] = secret
            
        return self._request('GET', '/api/session/question', params=params)
    
    def run_interview_action(self, i: str, session: str, action: str, secret: Optional[str] = None,
                            persistent: bool = False, arguments: Optional[Dict] = None,
                            overwrite: bool = False, read_only: bool = False) -> Optional[str]:
        """
        Führt eine Aktion in einem Interview aus
        
        Benötigte Berechtigungen: Keine
        
        Args:
            i: Interview Dateiname
            session: Session ID
            action: Name der auszuführenden Aktion
            secret: Entschlüsselungskey (falls verschlüsselt)
            persistent: Ob Aktion eine Frage zeigen soll
            arguments: Argumente für die Aktion
            overwrite: Ob vorherige Antworten überschrieben werden sollen
            read_only: Ob Antworten gespeichert werden sollen
            
        Returns:
            Response Content oder None
        """
        data = {'i': i, 'session': session, 'action': action}
        if secret:
            data['secret'] = secret
        if persistent:
            data['persistent'] = '1'
        if arguments:
            data['arguments'] = arguments
        if overwrite:
            data['overwrite'] = '1'
        if read_only:
            data['read_only'] = '1'
            
        return self._request('POST', '/api/session/action', data=data)
    
    def go_back_in_interview(self, i: str, session: str, secret: Optional[str] = None,
                            question: bool = True) -> Optional[Dict[str, Any]]:
        """
        Geht einen Schritt zurück in der Interview Session
        
        Benötigte Berechtigungen: Keine
        
        Args:
            i: Interview Dateiname
            session: Session ID
            secret: Entschlüsselungskey (falls verschlüsselt)
            question: Ob aktuelle Frage zurückgegeben werden soll
            
        Returns:
            JSON der aktuellen Frage oder None wenn question=False
        """
        data = {'i': i, 'session': session}
        if secret:
            data['secret'] = secret
        if not question:
            data['question'] = '0'
            
        return self._request('POST', '/api/session/back', data=data)
    
    def delete_interview_session(self, i: str, session: str) -> None:
        """
        Löscht eine Interview Session
        
        Benötigte Berechtigungen: Keine
        
        Args:
            i: Interview Dateiname
            session: Session ID
        """
        params = {'i': i, 'session': session}
        return self._request('DELETE', '/api/session', params=params)
    
    def retrieve_stored_file(self, file_number: int) -> bytes:
        """
        Lädt eine gespeicherte Datei herunter
        
        Benötigte Berechtigungen: Abhängig vom Dateizugriff
        
        Args:
            file_number: Datei Nummer
            
        Returns:
            Dateiinhalt als Bytes
        """
        return self._request('GET', f'/api/file/{file_number}')

    # ====================================================================
    # PLAYGROUND (9 Endpunkte)
    # ====================================================================
    
    def list_playground_files(self, user_id: Optional[int] = None, folder: str = 'static',
                             project: str = 'default', filename: Optional[str] = None) -> Union[List[str], str, bytes]:
        """
        Listet Dateien im Playground oder lädt eine spezifische Datei
        
        Benötigte Berechtigungen: admin, developer oder playground_control
        
        Args:
            user_id: Benutzer ID (optional, nur admins können andere Benutzer zugreifen)
            folder: Ordner ('questions', 'sources', 'static', 'templates', 'modules', 'packages')
            project: Projekt Name (default: 'default')
            filename: Dateiname zum Download (optional)
            
        Returns:
            Liste der Dateien oder Dateiinhalt wenn filename angegeben
        """
        params = {'folder': folder, 'project': project}
        if user_id:
            params['user_id'] = user_id
        if filename:
            params['filename'] = filename
            
        return self._request('GET', '/api/playground', params=params)
    
    def delete_playground_file(self, filename: str, user_id: Optional[int] = None,
                              folder: str = 'static', project: str = 'default') -> Optional[Dict[str, str]]:
        """
        Löscht eine Datei aus dem Playground
        
        Benötigte Berechtigungen: admin, developer oder playground_control
        
        Args:
            filename: Dateiname zum Löschen
            user_id: Benutzer ID (optional)
            folder: Ordner Name
            project: Projekt Name
            
        Returns:
            Task ID für Restart wenn nötig, sonst None
        """
        params = {'filename': filename, 'folder': folder, 'project': project}
        if user_id:
            params['user_id'] = user_id
            
        return self._request('DELETE', '/api/playground', params=params)
    
    def upload_playground_files(self, files: Dict[str, Any], user_id: Optional[int] = None,
                               folder: str = 'static', project: str = 'default') -> Optional[Dict[str, str]]:
        """
        Lädt Dateien in den Playground hoch
        
        Benötigte Berechtigungen: admin, developer oder playground_control
        
        Args:
            files: Dict mit Datei-Uploads
            user_id: Benutzer ID (optional)
            folder: Zielordner
            project: Zielprojekt
            
        Returns:
            Task ID für Restart wenn nötig, sonst None
        """
        data = {'folder': folder, 'project': project}
        if user_id:
            data['user_id'] = user_id
            
        return self._request('POST', '/api/playground', data=data, files=files)
    
    def install_playground_packages(self, packages: Dict[str, Any], user_id: Optional[int] = None,
                                   project: str = 'default', restart: bool = True) -> Optional[Dict[str, str]]:
        """
        Installiert Packages in den Playground
        
        Benötigte Berechtigungen: admin, developer oder playground_control
        
        Args:
            packages: Dict mit Package ZIP Dateien
            user_id: Benutzer ID (optional)
            project: Zielprojekt
            restart: Ob Server nach Installation restartet werden soll
            
        Returns:
            Task ID für Restart wenn nötig, sonst None
        """
        data = {'project': project}
        if user_id:
            data['user_id'] = user_id
        if not restart:
            data['restart'] = '0'
            
        return self._request('POST', '/api/playground_install', data=data, files=packages)
    
    def list_playground_projects(self, user_id: Optional[int] = None) -> List[str]:
        """
        Listet Projekte im Playground
        
        Benötigte Berechtigungen: admin, developer oder playground_control
        
        Args:
            user_id: Benutzer ID (optional)
            
        Returns:
            Liste der Projekt Namen
        """
        params = {}
        if user_id:
            params['user_id'] = user_id
            
        return self._request('GET', '/api/playground/project', params=params)
    
    def delete_playground_project(self, name: str, user_id: Optional[int] = None) -> None:
        """
        Löscht ein Projekt aus dem Playground
        
        Benötigte Berechtigungen: admin, developer oder playground_control
        
        Args:
            name: Projekt Name
            user_id: Benutzer ID (optional)
        """
        params = {'name': name}
        if user_id:
            params['user_id'] = user_id
            
        return self._request('DELETE', '/api/projects', params=params)
    
    def create_playground_project(self, name: str, user_id: Optional[int] = None) -> None:
        """
        Erstellt ein neues Projekt im Playground
        
        Benötigte Berechtigungen: admin, developer oder playground_control
        
        Args:
            name: Projekt Name
            user_id: Benutzer ID (optional)
        """
        data = {'name': name}
        if user_id:
            data['user_id'] = user_id
            
        return self._request('POST', '/api/projects', data=data)
    
    def pull_package_to_playground(self, user_id: Optional[int] = None, project: str = 'default',
                                  github_url: Optional[str] = None, branch: Optional[str] = None,
                                  pip: Optional[str] = None, restart: bool = True) -> Optional[Dict[str, str]]:
        """
        Zieht ein Package in den Playground
        
        Benötigte Berechtigungen: admin, developer oder playground_control
        
        Args:
            user_id: Benutzer ID (optional)
            project: Zielprojekt
            github_url: GitHub URL zum Pullen
            branch: Git Branch (optional)
            pip: PyPI Package Name
            restart: Ob Server restartet werden soll
            
        Returns:
            Task ID für Restart wenn nötig, sonst None
        """
        data = {'project': project}
        if user_id:
            data['user_id'] = user_id
        if github_url:
            data['github_url'] = github_url
        if branch:
            data['branch'] = branch
        if pip:
            data['pip'] = pip
        if not restart:
            data['restart'] = '0'
            
        return self._request('POST', '/api/playground/pull', data=data)
    
    def clear_interview_cache(self) -> None:
        """
        Löscht den Interview Cache
        
        Benötigte Berechtigungen: admin, developer oder playground_control
        """
        return self._request('POST', '/api/clear_cache', data={})

    # ====================================================================
    # SYSTEM ADMINISTRATION (8 Endpunkte)
    # ====================================================================
    
    def get_server_config(self) -> Dict[str, Any]:
        """
        Holt die Server Konfiguration
        
        Benötigte Berechtigungen: admin
        
        Returns:
            Server Konfiguration als JSON
        """
        return self._request('GET', '/api/config')
    
    def write_server_config(self, config: Dict[str, Any]) -> Dict[str, str]:
        """
        Schreibt eine neue Server Konfiguration
        
        Benötigte Berechtigungen: admin
        
        Args:
            config: Neue Konfiguration als Dict
            
        Returns:
            Task ID für Restart
        """
        return self._request('POST', '/api/config', data={'config': config})
    
    def update_server_config(self, config_changes: Dict[str, Any]) -> Dict[str, str]:
        """
        Aktualisiert spezifische Konfigurationsdirektiven
        
        Benötigte Berechtigungen: admin
        
        Args:
            config_changes: Dict mit zu ändernden Konfigurationswerten
            
        Returns:
            Task ID für Restart
        """
        return self._request('PATCH', '/api/config', data={'config_changes': config_changes})
    
    def list_installed_packages(self) -> List[Dict[str, Any]]:
        """
        Listet installierte Python Packages
        
        Benötigte Berechtigungen: admin oder developer
        
        Returns:
            Liste der installierten Packages mit Details
        """
        return self._request('GET', '/api/package')
    
    def install_or_update_package(self, update: Optional[str] = None, github_url: Optional[str] = None,
                                 branch: Optional[str] = None, pip: Optional[str] = None,
                                 zip_file: Optional[Any] = None, restart: bool = True) -> Dict[str, str]:
        """
        Installiert oder aktualisiert ein Package
        
        Benötigte Berechtigungen: admin oder developer
        
        Args:
            update: Package Name zum Aktualisieren
            github_url: GitHub URL für Installation
            branch: Git Branch (optional)
            pip: PyPI Package Name
            zip_file: ZIP Datei Upload
            restart: Ob Server restartet werden soll
            
        Returns:
            Task ID für Package Update Monitoring
        """
        data = {}
        if update:
            data['update'] = update
        if github_url:
            data['github_url'] = github_url
        if branch:
            data['branch'] = branch
        if pip:
            data['pip'] = pip
        if not restart:
            data['restart'] = '0'
            
        files = {}
        if zip_file:
            files['zip'] = zip_file
            
        return self._request('POST', '/api/package', data=data, files=files if files else None)
    
    def install_package(self, package: Optional[str] = None, github_url: Optional[str] = None,
                       branch: Optional[str] = None, pip: Optional[str] = None,
                       zip_file: Optional[Any] = None, restart: bool = True) -> Dict[str, str]:
        """
        Installiert ein Package (Alias für install_or_update_package)
        
        Benötigte Berechtigungen: admin oder developer
        
        Args:
            package: Package Name (GitHub URL, PyPI name oder ZIP)
            github_url: GitHub URL für Installation
            branch: Git Branch (optional)
            pip: PyPI Package Name
            zip_file: ZIP Datei Upload
            restart: Ob Server restartet werden soll
            
        Returns:
            Task ID für Package Update Monitoring
        """
        # Vereinfachte Logik: versuche automatisch zu erkennen was für ein Package es ist
        if package and package.startswith('http'):
            github_url = package
        elif package and not pip and not github_url:
            pip = package
            
        return self.install_or_update_package(
            github_url=github_url, branch=branch, pip=pip, 
            zip_file=zip_file, restart=restart
        )
    
    def uninstall_package(self, package: str, restart: bool = True) -> Dict[str, str]:
        """
        Deinstalliert ein Package
        
        Benötigte Berechtigungen: admin oder developer
        
        Args:
            package: Package Name zum Deinstallieren
            restart: Ob Server restartet werden soll
            
        Returns:
            Task ID für Package Update Monitoring
        """
        params = {'package': package}
        if not restart:
            params['restart'] = '0'
            
        return self._request('DELETE', '/api/package', params=params)
    
    def get_package_update_status(self, task_id: str) -> Dict[str, Any]:
        """
        Überprüft Status eines Package Update Prozesses
        
        Benötigte Berechtigungen: admin oder developer
        
        Args:
            task_id: Task ID vom Package Update
            
        Returns:
            Status Information des Update Prozesses
        """
        return self._request('GET', '/api/package_update_status', params={'task_id': task_id})
    
    def trigger_server_restart(self) -> Dict[str, str]:
        """
        Löst einen Server Restart aus
        
        Benötigte Berechtigungen: admin, developer oder playground_control
        
        Returns:
            Task ID für Restart Monitoring
        """
        return self._request('POST', '/api/restart', data={})
    
    def get_restart_status(self, task_id: str) -> Dict[str, Any]:
        """
        Überprüft Status eines Server Restarts
        
        Benötigte Berechtigungen: admin, developer oder playground_control
        
        Args:
            task_id: Task ID vom Restart
            
        Returns:
            Status Information des Restart Prozesses
        """
        return self._request('GET', '/api/restart_status', params={'task_id': task_id})

    # ====================================================================
    # API KEY MANAGEMENT (8 Endpunkte)
    # ====================================================================
    
    def get_user_api_keys(self, api_key: Optional[str] = None, name: Optional[str] = None) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Holt API Key Informationen des aktuellen Benutzers
        
        Benötigte Berechtigungen: Keine
        
        Args:
            api_key: Spezifischer API Key (optional)
            name: API Key Name (optional)
            
        Returns:
            API Key Details oder Liste aller API Keys
        """
        params = {}
        if api_key:
            params['api_key'] = api_key
        if name:
            params['name'] = name
            
        return self._request('GET', '/api/user/api', params=params)
    
    def delete_user_api_key(self, api_key: str) -> None:
        """
        Löscht einen API Key des aktuellen Benutzers
        
        Benötigte Berechtigungen: Keine
        
        Args:
            api_key: API Key zum Löschen
        """
        return self._request('DELETE', '/api/user/api', params={'api_key': api_key})
    
    def create_user_api_key(self, name: str, method: str = 'none', allowed: Optional[List[str]] = None,
                           permissions: Optional[List[str]] = None) -> str:
        """
        Erstellt einen neuen API Key für den aktuellen Benutzer
        
        Benötigte Berechtigungen: Keine
        
        Args:
            name: Name des API Keys
            method: Zugriffsmethode ('ip', 'referer', 'none')
            allowed: Liste erlaubter IPs oder URLs
            permissions: Liste beschränkter Berechtigungen (nur für admins)
            
        Returns:
            Neuer API Key als String
        """
        data = {'name': name, 'method': method}
        if allowed:
            data['allowed'] = allowed
        if permissions:
            data['permissions'] = permissions
            
        return self._request('POST', '/api/user/api', data=data)
    
    def update_user_api_key(self, api_key: Optional[str] = None, name: Optional[str] = None,
                           method: Optional[str] = None, allowed: Optional[List[str]] = None,
                           add_to_allowed: Optional[Union[str, List[str]]] = None,
                           remove_from_allowed: Optional[Union[str, List[str]]] = None,
                           permissions: Optional[List[str]] = None,
                           add_to_permissions: Optional[Union[str, List[str]]] = None,
                           remove_from_permissions: Optional[Union[str, List[str]]] = None) -> None:
        """
        Aktualisiert einen API Key des aktuellen Benutzers
        
        Benötigte Berechtigungen: Keine
        
        Args:
            api_key: API Key zum Modifizieren (optional, default: aktueller Key)
            name: Neuer Name
            method: Neue Zugriffsmethode
            allowed: Neue Liste erlaubter Origins
            add_to_allowed: Zu allowed hinzuzufügende Items
            remove_from_allowed: Aus allowed zu entfernende Items
            permissions: Neue Berechtigungsliste
            add_to_permissions: Zu permissions hinzuzufügende Items
            remove_from_permissions: Aus permissions zu entfernende Items
        """
        data = {}
        if api_key:
            data['api_key'] = api_key
        if name:
            data['name'] = name
        if method:
            data['method'] = method
        if allowed:
            data['allowed'] = allowed
        if add_to_allowed:
            data['add_to_allowed'] = add_to_allowed
        if remove_from_allowed:
            data['remove_from_allowed'] = remove_from_allowed
        if permissions:
            data['permissions'] = permissions
        if add_to_permissions:
            data['add_to_permissions'] = add_to_permissions
        if remove_from_permissions:
            data['remove_from_permissions'] = remove_from_permissions
            
        return self._request('PATCH', '/api/user/api', data=data)
    
    def get_user_api_keys_by_id(self, user_id: int, api_key: Optional[str] = None,
                               name: Optional[str] = None) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Holt API Key Informationen eines bestimmten Benutzers
        
        Benötigte Berechtigungen: admin, eigene ID oder access_user_api_info
        
        Args:
            user_id: Benutzer ID
            api_key: Spezifischer API Key (optional)
            name: API Key Name (optional)
            
        Returns:
            API Key Details oder Liste aller API Keys des Benutzers
        """
        params = {}
        if api_key:
            params['api_key'] = api_key
        if name:
            params['name'] = name
            
        return self._request('GET', f'/api/user/{user_id}/api', params=params)
    
    def delete_user_api_key_by_id(self, user_id: int, api_key: str) -> None:
        """
        Löscht einen API Key eines bestimmten Benutzers
        
        Benötigte Berechtigungen: admin, eigene ID oder (access_user_api_info und edit_user_api_info)
        
        Args:
            user_id: Benutzer ID
            api_key: API Key zum Löschen
        """
        return self._request('DELETE', f'/api/user/{user_id}/api', params={'api_key': api_key})
    
    def create_user_api_key_by_id(self, user_id: int, name: str, method: str = 'none',
                                 allowed: Optional[List[str]] = None,
                                 permissions: Optional[List[str]] = None) -> str:
        """
        Erstellt einen neuen API Key für einen bestimmten Benutzer
        
        Benötigte Berechtigungen: admin, eigene ID oder (access_user_api_info und edit_user_api_info)
        
        Args:
            user_id: Benutzer ID
            name: Name des API Keys
            method: Zugriffsmethode ('ip', 'referer', 'none')
            allowed: Liste erlaubter IPs oder URLs
            permissions: Liste beschränkter Berechtigungen
            
        Returns:
            Neuer API Key als String
        """
        data = {'name': name, 'method': method}
        if allowed:
            data['allowed'] = allowed
        if permissions:
            data['permissions'] = permissions
            
        return self._request('POST', f'/api/user/{user_id}/api', data=data)
    
    def update_user_api_key_by_id(self, user_id: int, api_key: str, name: Optional[str] = None,
                                 method: Optional[str] = None, allowed: Optional[List[str]] = None,
                                 add_to_allowed: Optional[Union[str, List[str]]] = None,
                                 remove_from_allowed: Optional[Union[str, List[str]]] = None,
                                 permissions: Optional[List[str]] = None,
                                 add_to_permissions: Optional[Union[str, List[str]]] = None,
                                 remove_from_permissions: Optional[Union[str, List[str]]] = None) -> None:
        """
        Aktualisiert einen API Key eines bestimmten Benutzers
        
        Benötigte Berechtigungen: admin, eigene ID oder (access_user_api_info und edit_user_api_info)
        
        Args:
            user_id: Benutzer ID
            api_key: API Key zum Modifizieren (erforderlich)
            name: Neuer Name
            method: Neue Zugriffsmethode
            allowed: Neue Liste erlaubter Origins
            add_to_allowed: Zu allowed hinzuzufügende Items
            remove_from_allowed: Aus allowed zu entfernende Items
            permissions: Neue Berechtigungsliste
            add_to_permissions: Zu permissions hinzuzufügende Items
            remove_from_permissions: Aus permissions zu entfernende Items
        """
        data = {'api_key': api_key}
        if name:
            data['name'] = name
        if method:
            data['method'] = method
        if allowed:
            data['allowed'] = allowed
        if add_to_allowed:
            data['add_to_allowed'] = add_to_allowed
        if remove_from_allowed:
            data['remove_from_allowed'] = remove_from_allowed
        if permissions:
            data['permissions'] = permissions
        if add_to_permissions:
            data['add_to_permissions'] = add_to_permissions
        if remove_from_permissions:
            data['remove_from_permissions'] = remove_from_permissions
            
        return self._request('PATCH', f'/api/user/{user_id}/api', data=data)

    # ====================================================================
    # FILE OPERATIONS (3 Endpunkte)
    # ====================================================================
    
    def extract_template_fields(self, template_file: Any, format: str = 'json') -> Union[Dict[str, Any], str]:
        """
        Extrahiert Felder aus einer Template Datei (PDF, DOCX, Markdown)
        
        Benötigte Berechtigungen: admin, developer oder template_parse
        
        Args:
            template_file: Template Datei (PDF oder DOCX)
            format: Ausgabeformat ('json' oder 'yaml')
            
        Returns:
            Feldinformationen als JSON Dict oder YAML String
        """
        data = {}
        if format != 'json':
            data['format'] = format
            
        files = {'template': template_file}
        
        return self._request('POST', '/api/fields', data=data, files=files)
    
    # NICHT-DOKUMENTIERTE ENDPUNKTE ENTFERNT  
    # convert_file_to_markdown existiert nicht in der offiziellen API
    
    def get_interview_data(self, i: str) -> Dict[str, Any]:
        """
        Holt Informationen über ein Interview (Python Namen, Variablen, etc.)
        
        Benötigte Berechtigungen: admin, developer oder interview_data
        
        Args:
            i: Interview Dateiname
            
        Returns:
            Interview Datenanalyse
        """
        return self._request('GET', '/api/interview_data', params={'i': i})

    # ====================================================================
    # DATA STASHING (2 Endpunkte)
    # ====================================================================
    
    # NICHT-DOKUMENTIERTE ENDPUNKTE ENTFERNT
    # stash_data und convert_file_to_markdown existieren nicht in der offiziellen API
    
    def retrieve_stashed_data(self, stash_key: str, secret: str, delete: bool = False,
                             refresh: Optional[int] = None) -> Any:
        """
        Holt temporär gespeicherte Daten
        
        Benötigte Berechtigungen: Keine
        
        Args:
            stash_key: Stash Schlüssel
            secret: Entschlüsselungsgeheimnis
            delete: Ob Daten nach Abruf gelöscht werden sollen
            refresh: Neue Ablaufzeit in Sekunden
            
        Returns:
            Gespeicherte Daten
        """
        params = {'stash_key': stash_key, 'secret': secret}
        if delete:
            params['delete'] = '1'
        if refresh is not None:
            params['refresh'] = refresh
            
        return self._request('GET', '/api/retrieve_stashed_data', params=params)

    # Convenience methods for direct usage (non-MCP)
    def list_interviews(self):
        """List all available interviews"""
        return self.list_advertised_interviews()
    
    def list_packages(self):
        """List all packages"""
        return self.list_package_management()
    
    def get_user_list(self):
        """Get list of users"""
        return self.list_users()
