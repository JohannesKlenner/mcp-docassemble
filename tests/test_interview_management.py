"""
Test Modul: Interview-Management API Endpunkte
Tests für alle interview-bezogenen Endpunkte
"""

import time
from typing import Dict, Tuple
from .test_base import APITestBase

class InterviewManagementTests(APITestBase):
    """Tests für Interview-Management Endpunkte"""
    
    def run_all_tests(self) -> Dict[str, Tuple[bool, str]]:
        """Führt alle Interview-Management Tests aus"""
        self.print_section_header("INTERVIEW-MANAGEMENT TESTS", 12)
        
        results = {}
        
        # Session-Management Tests
        results['start_interview'] = self.test_endpoint(
            'start_interview', self._test_start_interview
        )
        
        results['get_interview_variables'] = self.test_endpoint(
            'get_interview_variables', self._test_get_interview_variables
        )
        
        results['set_interview_variables'] = self.test_endpoint(
            'set_interview_variables', self._test_set_interview_variables
        )
        
        results['get_current_question'] = self.test_endpoint(
            'get_current_question', self._test_get_current_question
        )
        
        results['run_interview_action'] = self.test_endpoint(
            'run_interview_action', self._test_run_interview_action
        )
        
        results['go_back_in_interview'] = self.test_endpoint(
            'go_back_in_interview', self._test_go_back_in_interview
        )
        
        results['delete_interview_session'] = self.test_endpoint(
            'delete_interview_session', self._test_delete_interview_session
        )
        
        # Listen-Management Tests
        results['list_interview_sessions'] = self.test_endpoint(
            'list_interview_sessions', self._test_list_interview_sessions
        )
        
        results['delete_interview_sessions'] = self.test_endpoint(
            'delete_interview_sessions', self._test_delete_interview_sessions
        )
        
        results['list_advertised_interviews'] = self.test_endpoint(
            'list_advertised_interviews', self._test_list_advertised_interviews
        )
        
        # Utility-Tests
        results['get_user_secret'] = self.test_endpoint(
            'get_user_secret', self._test_get_user_secret
        )
        
        results['get_login_url'] = self.test_endpoint(
            'get_login_url', self._test_get_login_url
        )
        
        self.print_results(results)
        return results
    
    def _test_start_interview(self):
        """Test: Interview starten"""
        return self.client.start_interview(
            i="docassemble.demo:data/questions/questions.yml"
        )
    
    def _test_get_interview_variables(self):
        """Test: Interview-Variablen holen"""
        # Erst Session erstellen
        session = self.client.start_interview(
            i="docassemble.demo:data/questions/questions.yml"
        )
        return self.client.get_interview_variables(
            i="docassemble.demo:data/questions/questions.yml",
            session=session['session'],
            secret=session.get('secret')
        )
    
    def _test_set_interview_variables(self):
        """Test: Interview-Variablen setzen"""
        # Erst Session erstellen
        session = self.client.start_interview(
            i="docassemble.demo:data/questions/questions.yml"
        )
        return self.client.set_interview_variables(
            i="docassemble.demo:data/questions/questions.yml",
            session=session['session'],
            variables={"test_var": "test_value"},
            secret=session.get('secret')
        )
    
    def _test_get_current_question(self):
        """Test: Aktuelle Frage holen"""
        # Erst Session erstellen
        session = self.client.start_interview(
            i="docassemble.demo:data/questions/questions.yml"
        )
        return self.client.get_current_question(
            i="docassemble.demo:data/questions/questions.yml",
            session=session['session'],
            secret=session.get('secret')
        )
    
    def _test_run_interview_action(self):
        """Test: Interview-Aktion ausführen"""
        # Dieser Test wird wahrscheinlich fehlschlagen (404), aber wir testen trotzdem
        return self.client.run_interview_action(
            i="docassemble.demo:data/questions/questions.yml",
            session="test_session",
            action="test_action"
        )
    
    def _test_go_back_in_interview(self):
        """Test: Im Interview zurückgehen"""
        return self.client.go_back_in_interview(
            i="docassemble.demo:data/questions/questions.yml",
            session="test_session"
        )
    
    def _test_delete_interview_session(self):
        """Test: Interview-Session löschen"""
        # Erst Session erstellen
        session = self.client.start_interview(
            i="docassemble.demo:data/questions/questions.yml"
        )
        return self.client.delete_interview_session(
            i="docassemble.demo:data/questions/questions.yml",
            session=session['session']
        )
    
    def _test_list_interview_sessions(self):
        """Test: Interview-Sessions auflisten"""
        return self.client.list_interview_sessions()
    
    def _test_delete_interview_sessions(self):
        """Test: Interview-Sessions löschen"""
        return self.client.delete_interview_sessions(
            i="docassemble.base:data/questions/examples/hello.yml"
        )
    
    def _test_list_advertised_interviews(self):
        """Test: Beworbene Interviews auflisten"""
        return self.client.list_advertised_interviews()
    
    def _test_get_user_secret(self):
        """Test: Benutzer-Secret holen"""
        return self.client.get_user_secret()
    
    def _test_get_login_url(self):
        """Test: Login-URL holen"""
        return self.client.get_login_url(next="/test")
