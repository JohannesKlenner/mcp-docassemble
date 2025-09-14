"""
Test Modul: Server-Management API Endpunkte
Tests für alle server-bezogenen Endpunkte
"""

import time
from typing import Dict, Tuple
from .test_base import APITestBase

class ServerManagementTests(APITestBase):
    """Tests für Server-Management Endpunkte"""
    
    def run_all_tests(self) -> Dict[str, Tuple[bool, str]]:
        """Führt alle Server-Management Tests aus"""
        self.print_section_header("SERVER-MANAGEMENT TESTS", 7)
        
        results = {}
        
        results['get_server_config'] = self.test_endpoint(
            'get_server_config', self._test_get_server_config
        )
        
        results['list_installed_packages'] = self.test_endpoint(
            'list_installed_packages', self._test_list_installed_packages
        )
        
        results['install_package'] = self.test_endpoint(
            'install_package', self._test_install_package
        )
        
        results['uninstall_package'] = self.test_endpoint(
            'uninstall_package', self._test_uninstall_package
        )
        
        results['get_package_update_status'] = self.test_endpoint(
            'get_package_update_status', self._test_get_package_update_status
        )
        
        results['trigger_server_restart'] = self.test_endpoint(
            'trigger_server_restart', self._test_trigger_server_restart
        )
        
        results['get_restart_status'] = self.test_endpoint(
            'get_restart_status', self._test_get_restart_status
        )
        
        self.print_results(results)
        return results
    
    def _test_get_server_config(self):
        """Test: Server-Konfiguration holen"""
        return self.client.get_server_config()
    
    def _test_list_installed_packages(self):
        """Test: Installierte Pakete auflisten"""
        return self.client.list_installed_packages()
    
    def _test_install_package(self):
        """Test: Paket installieren"""
        # Versuche ein kleines, harmloses Paket zu installieren
        return self.client.install_package(pip="requests")
    
    def _test_uninstall_package(self):
        """Test: Paket deinstallieren"""
        # Test mit einem Paket-Namen (kann fehlschlagen wenn nicht installiert)
        return self.client.uninstall_package(package="test-package")
    
    def _test_get_package_update_status(self):
        """Test: Paket-Update-Status holen"""
        # Test mit einer erfundenen Task-ID
        return self.client.get_package_update_status(task_id="test_task_id")
    
    def _test_trigger_server_restart(self):
        """Test: Server-Neustart auslösen"""
        return self.client.trigger_server_restart()
    
    def _test_get_restart_status(self):
        """Test: Neustart-Status holen"""
        # Test mit einer erfundenen Task-ID
        return self.client.get_restart_status(task_id="test_task_id")
