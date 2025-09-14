"""
Test Modul: Daten & API-Key Management
Tests für alle daten-bezogenen und API-Schlüssel Endpunkte
"""

import time
from typing import Dict, Tuple
from .test_base import APITestBase

class DataAndKeyManagementTests(APITestBase):
    """Tests für Daten- und API-Key-Management Endpunkte"""
    
    def run_all_tests(self) -> Dict[str, Tuple[bool, str]]:
        """Führt alle Daten- und API-Key Tests aus"""
        self.print_section_header("DATEN & API-KEY MANAGEMENT TESTS", 7)
        
        results = {}
        
        # API-Key Tests
        results['get_user_api_keys'] = self.test_endpoint(
            'get_user_api_keys', self._test_get_user_api_keys
        )
        
        results['create_user_api_key'] = self.test_endpoint(
            'create_user_api_key', self._test_create_user_api_key
        )
        
        results['delete_user_api_key'] = self.test_endpoint(
            'delete_user_api_key', self._test_delete_user_api_key
        )
        
        # Daten Tests
        results['get_interview_data'] = self.test_endpoint(
            'get_interview_data', self._test_get_interview_data
        )
        
        results['retrieve_stashed_data'] = self.test_endpoint(
            'retrieve_stashed_data', self._test_retrieve_stashed_data
        )
        
        self.print_results(results)
        return results
    
    def _test_get_user_api_keys(self):
        """Test: Benutzer-API-Keys holen"""
        return self.client.get_user_api_keys()
    
    def _test_create_user_api_key(self):
        """Test: Benutzer-API-Key erstellen"""
        return self.client.create_user_api_key(
            name=f"test_key_{int(time.time())}",
            method="none"
        )
    
    def _test_delete_user_api_key(self):
        """Test: Benutzer-API-Key löschen"""
        # Erst einen Key erstellen, dann löschen
        try:
            key_result = self.client.create_user_api_key(
                name=f"to_delete_{int(time.time())}",
                method="none"
            )
            # Extrahiere den API-Key aus der Antwort
            if isinstance(key_result, str):
                api_key = key_result
            else:
                api_key = key_result.get('key', 'dummy_key')
            
            return self.client.delete_user_api_key(api_key=api_key)
        except Exception as e:
            return {"error": f"Could not create key to delete: {e}"}
    
    def _test_get_interview_data(self):
        """Test: Interview-Daten holen"""
        return self.client.get_interview_data(
            i="docassemble.demo:data/questions/questions.yml"
        )
    
    def _test_retrieve_stashed_data(self):
        """Test: Gestashte Daten holen"""
        # Da wir stash_data entfernt haben, ist das ein Test mit ungültigen Daten
        return self.client.retrieve_stashed_data(
            stash_key="invalid_key",
            secret="invalid_secret"
        )
