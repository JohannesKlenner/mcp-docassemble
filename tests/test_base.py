"""
Test Base - Gemeinsame Funktionen für alle API-Tests
"""

import time
from typing import Dict, Any, Tuple
from src.mcp_docassemble.client import DocassembleClient, DocassembleAPIError

class APITestBase:
    """Basis-Klasse für alle API-Tests mit gemeinsamen Funktionen"""
    
    def __init__(self):
        self.base_url = "http://192.168.178.29"
        self.api_key = "X1IgbwNOk0b0LQ6LS46eSYfj8Ycj4ICU"
        self.client = DocassembleClient(self.base_url, self.api_key)
        self.delay = 2  # Sekunden zwischen Tests
    
    def test_endpoint(self, endpoint_name: str, test_function) -> Tuple[bool, str]:
        """
        Führt einen einzelnen Endpunkt-Test aus
        
        Args:
            endpoint_name: Name des Endpunkts für Logging
            test_function: Funktion, die den Test durchführt
            
        Returns:
            Tuple[bool, str]: (Erfolg, Beschreibung)
        """
        print(f"\n🔄 Teste: {endpoint_name}")
        print("-" * 50)
        
        try:
            result = test_function()
            print(f"✅ ERFOLG: {result}")
            time.sleep(self.delay)  # Rate limiting
            return True, f"{endpoint_name} funktioniert korrekt"
            
        except DocassembleAPIError as e:
            print(f"❌ API FEHLER: {e}")
            
            # Analysiere den Fehler
            if e.status_code == 404:
                return False, f"404 - Endpunkt nicht gefunden: {e}"
            elif e.status_code == 403:
                return False, f"403 - Keine Berechtigung: {e}"
            elif e.status_code == 400:
                return False, f"400 - Ungültige Parameter: {e}"
            else:
                return False, f"Unbekannter Fehler ({e.status_code}): {e}"
                
        except Exception as e:
            print(f"❌ SYSTEM FEHLER: {e}")
            return False, f"System-Fehler: {e}"
    
    def print_section_header(self, section_name: str, total_endpoints: int):
        """Druckt einen formatierten Abschnittsheader"""
        print(f"\n{'='*60}")
        print(f"🧪 {section_name}")
        print(f"📊 {total_endpoints} Endpunkte zu testen")
        print(f"{'='*60}")
    
    def print_results(self, results: Dict[str, Tuple[bool, str]]):
        """Druckt die Ergebnisse einer Test-Kategorie"""
        successful = sum(1 for success, _ in results.values() if success)
        total = len(results)
        
        print(f"\n📊 ERGEBNISSE ({successful}/{total} erfolgreich):")
        print("-" * 50)
        
        for endpoint, (success, message) in results.items():
            status = "✅" if success else "❌"
            print(f"{status} {endpoint}: {message}")
        
        return successful, total
