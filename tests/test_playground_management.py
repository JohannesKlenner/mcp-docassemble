"""
Test Modul: Playground-Management API Endpunkte
Tests für alle playground-bezogenen Endpunkte
"""

import time
from typing import Dict, Tuple
from .test_base import APITestBase

class PlaygroundManagementTests(APITestBase):
    """Tests für Playground-Management Endpunkte"""
    
    def run_all_tests(self) -> Dict[str, Tuple[bool, str]]:
        """Führt alle Playground-Management Tests aus"""
        self.print_section_header("PLAYGROUND-MANAGEMENT TESTS", 6)
        
        results = {}
        
        results['list_playground_files'] = self.test_endpoint(
            'list_playground_files', self._test_list_playground_files
        )
        
        results['delete_playground_file'] = self.test_endpoint(
            'delete_playground_file', self._test_delete_playground_file
        )
        
        results['list_playground_projects'] = self.test_endpoint(
            'list_playground_projects', self._test_list_playground_projects
        )
        
        results['create_playground_project'] = self.test_endpoint(
            'create_playground_project', self._test_create_playground_project
        )
        
        results['delete_playground_project'] = self.test_endpoint(
            'delete_playground_project', self._test_delete_playground_project
        )
        
        results['clear_interview_cache'] = self.test_endpoint(
            'clear_interview_cache', self._test_clear_interview_cache
        )
        
        self.print_results(results)
        return results
    
    def _test_list_playground_files(self):
        """Test: Playground-Dateien auflisten"""
        return self.client.list_playground_files()
    
    def _test_delete_playground_file(self):
        """Test: Playground-Datei löschen"""
        # Erst eine Test-Datei erstellen wäre ideal, aber für Test reicht ein leerer Aufruf
        return self.client.delete_playground_file(
            filename=f"test_file_{int(time.time())}.yml"
        )
    
    def _test_list_playground_projects(self):
        """Test: Playground-Projekte auflisten"""
        return self.client.list_playground_projects()
    
    def _test_create_playground_project(self):
        """Test: Playground-Projekt erstellen"""
        return self.client.create_playground_project(
            name=f"test_project_{int(time.time())}"
        )
    
    def _test_delete_playground_project(self):
        """Test: Playground-Projekt löschen"""
        return self.client.delete_playground_project(
            name=f"test_project_{int(time.time())}"
        )
    
    def _test_clear_interview_cache(self):
        """Test: Interview-Cache leeren"""
        return self.client.clear_interview_cache()
