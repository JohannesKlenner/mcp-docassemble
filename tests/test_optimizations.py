# 🔧 Test-Optimierungen für verbleibende Probleme

import logging
from .test_base import BaseTest

class OptimizedFailureTests(BaseTest):
    """
    Optimierte Tests für die 4 einfach behebbaren API-Probleme
    Erwartete Verbesserung: +9.5% Erfolgsrate (von 81% auf 90.5%)
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Optimized Failure Tests"
        self.test_functions = [
            ('get_user_secret_fixed', self._test_get_user_secret_fixed),
            ('get_login_url_fixed', self._test_get_login_url_fixed),
            ('uninstall_package_fixed', self._test_uninstall_package_fixed),
            ('stash_retrieve_workflow', self._test_stash_retrieve_workflow)
        ]
    
    def _test_get_user_secret_fixed(self):
        """
        ✅ KORRIGIERT: get_user_secret mit erforderlichen Parametern
        Original Problem: Aufruf ohne Parameter
        """
        try:
            # Korrigierter Aufruf mit erforderlichen Parametern
            result = self.client.get_user_secret(
                username="admin",  # Server-Admin Username
                password="password"  # Standard-Passwort
            )
            
            logging.info(f"✅ get_user_secret_fixed: {result}")
            return result, None
            
        except Exception as e:
            logging.error(f"❌ get_user_secret_fixed failed: {e}")
            return None, e
    
    def _test_get_login_url_fixed(self):
        """
        ✅ KORRIGIERT: get_login_url mit next_page Parameter
        Original Problem: Falscher Parameter-Name (next → next_page)
        """
        try:
            # Korrigierter Aufruf mit korrektem Parameter-Namen
            result = self.client.get_login_url(
                next_page="/list"  # Korrekt: next_page statt next
            )
            
            logging.info(f"✅ get_login_url_fixed: {result}")
            return result, None
            
        except Exception as e:
            logging.error(f"❌ get_login_url_fixed failed: {e}")
            return None, e
    
    def _test_uninstall_package_fixed(self):
        """
        ✅ KORRIGIERT: uninstall_package mit existierendem Package
        Original Problem: Test-Package "test-package" existiert nicht
        """
        try:
            # Verwende existierendes Package anstatt Test-Package
            result = self.client.uninstall_package(
                package="docassemble.demo"  # Existierendes Standard-Package
            )
            
            logging.info(f"✅ uninstall_package_fixed: {result}")
            return result, None
            
        except Exception as e:
            logging.error(f"❌ uninstall_package_fixed failed: {e}")
            return None, e
    
    def _test_stash_retrieve_workflow(self):
        """
        ✅ KORRIGIERT: Vollständiger Stash-Workflow
        Original Problem: retrieve_stashed_data ohne vorherige stash_data
        """
        try:
            # Schritt 1: Daten speichern
            test_data = {
                "test_key": "test_value",
                "timestamp": "2024-01-01T00:00:00Z",
                "metadata": {"source": "optimization_test"}
            }
            
            stash_result = self.client.stash_data(data=test_data)
            logging.info(f"📦 Daten gespeichert: {stash_result}")
            
            if not stash_result or 'key' not in stash_result:
                raise Exception("stash_data lieferte keinen gültigen Key zurück")
            
            # Schritt 2: Daten abrufen mit korrekten Parametern
            retrieve_result = self.client.retrieve_stashed_data(
                stash_key=stash_result['key'],
                secret=stash_result.get('secret', 'default_secret')
            )
            
            logging.info(f"✅ stash_retrieve_workflow: {retrieve_result}")
            return retrieve_result, None
            
        except Exception as e:
            logging.error(f"❌ stash_retrieve_workflow failed: {e}")
            return None, e

# Zusätzliche Hilfsfunktionen für erweiterte Tests

class SessionHandlingTests(BaseTest):
    """
    Erweiterte Tests für Session-spezifische Probleme
    Für komplexere Fixes nach Server-Optimierung
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Session Handling Tests"
        self.test_functions = [
            ('go_back_with_session', self._test_go_back_with_session)
        ]
    
    def _test_go_back_with_session(self):
        """
        🟡 EXPERIMENTELL: go_back_in_interview mit realer Session
        Erfordert aktive Interview-Session
        """
        try:
            # Erst eine Interview-Session starten
            interview_result = self.client.run_interview(
                interview_name="docassemble.demo:data/questions/basic.yml"
            )
            
            if not interview_result or 'session' not in interview_result:
                raise Exception("Konnte keine Interview-Session starten")
            
            session_id = interview_result['session']
            
            # Dann zurück navigieren
            result = self.client.go_back_in_interview(
                session=session_id,
                steps=1
            )
            
            logging.info(f"✅ go_back_with_session: {result}")
            return result, None
            
        except Exception as e:
            logging.error(f"❌ go_back_with_session failed: {e}")
            return None, e

# Erweiterte Test-Runner

class OptimizedTestRunner:
    """
    Spezieller Test-Runner für die optimierten Tests
    """
    
    def __init__(self):
        self.tests = [
            OptimizedFailureTests(),
            SessionHandlingTests()
        ]
    
    def run_optimization_tests(self):
        """
        Führt nur die Optimierungs-Tests aus
        Erwartete Verbesserung: 4 zusätzliche erfolgreiche Endpunkte
        """
        results = {
            'total_tests': 0,
            'successful': 0,
            'failed': 0,
            'improvements': {},
            'detailed_results': {}
        }
        
        for test_suite in self.tests:
            suite_results = test_suite.run_tests()
            
            results['total_tests'] += suite_results['total']
            results['successful'] += suite_results['successful']
            results['failed'] += suite_results['failed']
            results['detailed_results'][test_suite.name] = suite_results
            
            # Verbesserungen tracken
            for test_name, (result, error) in suite_results['results'].items():
                if result is not None:
                    results['improvements'][test_name] = "✅ VERBESSERT"
                else:
                    results['improvements'][test_name] = f"❌ Weiterhin problematisch: {error}"
        
        # Erfolgsrate berechnen
        if results['total_tests'] > 0:
            success_rate = (results['successful'] / results['total_tests']) * 100
            results['success_rate'] = f"{success_rate:.1f}%"
        
        return results

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("🔧 STARTE OPTIMIERTE TEST-FIXES...")
    print("Erwartete Verbesserung: 81% → 90.5% Erfolgsrate")
    print("=" * 60)
    
    runner = OptimizedTestRunner()
    results = runner.run_optimization_tests()
    
    print("\n📊 OPTIMIERUNGS-ERGEBNISSE:")
    print(f"Getestete Fixes: {results['total_tests']}")
    print(f"Erfolgreiche Fixes: {results['successful']}")
    print(f"Erfolgsrate: {results.get('success_rate', 'N/A')}")
    
    print("\n🎯 VERBESSERUNGEN:")
    for test_name, status in results['improvements'].items():
        print(f"  {test_name}: {status}")
