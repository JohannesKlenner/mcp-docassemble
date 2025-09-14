#!/usr/bin/env python3
"""
Modularer Test-Runner für alle MCP Docassemble API Endpunkte

Führt systematische Tests in separaten Modulen durch für bessere
Übersichtlichkeit und Fehlerdiagnose.
"""

import sys
import time
from typing import Dict, Tuple, List
from tests.test_user_management import UserManagementTests
from tests.test_interview_management import InterviewManagementTests
from tests.test_playground_management import PlaygroundManagementTests
from tests.test_server_management import ServerManagementTests
from tests.test_data_and_keys import DataAndKeyManagementTests

class MasterTestRunner:
    """Haupt-Test-Runner für alle API-Kategorien"""
    
    def __init__(self):
        self.all_results = {}
        self.start_time = time.time()
    
    def run_all_tests(self):
        """Führt alle Test-Module aus"""
        print("🚀 MCP DOCASSEMBLE API - MODULARER VOLLTEST")
        print("=" * 70)
        print(f"⏰ Start: {time.strftime('%H:%M:%S')}")
        print(f"🌐 Server: http://192.168.178.29")
        print(f"🔑 API Key: X1IgbwNOk0b0LQ6LS46eSYfj8Ycj4ICU")
        print("=" * 70)
        
        # Führe alle Test-Module aus
        test_modules = [
            ("Benutzer-Management", UserManagementTests()),
            ("Interview-Management", InterviewManagementTests()),
            ("Playground-Management", PlaygroundManagementTests()),
            ("Server-Management", ServerManagementTests()),
            ("Daten & API-Keys", DataAndKeyManagementTests())
        ]
        
        total_successful = 0
        total_tests = 0
        
        for module_name, test_module in test_modules:
            print(f"\n🔄 Starte {module_name} Tests...")
            
            try:
                results = test_module.run_all_tests()
                self.all_results[module_name] = results
                
                # Zähle Erfolge
                successful = sum(1 for success, _ in results.values() if success)
                total_successful += successful
                total_tests += len(results)
                
                print(f"✅ {module_name}: {successful}/{len(results)} erfolgreich")
                
            except Exception as e:
                print(f"❌ FEHLER in {module_name}: {e}")
                self.all_results[module_name] = {"error": (False, str(e))}
        
        # Gesamt-Zusammenfassung
        self.print_final_summary(total_successful, total_tests)
    
    def print_final_summary(self, total_successful: int, total_tests: int):
        """Druckt die finale Zusammenfassung aller Tests"""
        duration = time.time() - self.start_time
        
        print(f"\n{'='*70}")
        print("📊 FINALE ZUSAMMENFASSUNG")
        print(f"{'='*70}")
        print(f"⏱️  Gesamtdauer: {duration:.1f} Sekunden")
        print(f"✅ Erfolgreich: {total_successful}/{total_tests} ({total_successful/total_tests*100:.1f}%)")
        print(f"❌ Fehlgeschlagen: {total_tests - total_successful}/{total_tests}")
        
        print(f"\n📋 DETAILS PRO KATEGORIE:")
        print("-" * 50)
        
        for module_name, results in self.all_results.items():
            if "error" in results:
                print(f"❌ {module_name}: MODUL-FEHLER")
            else:
                successful = sum(1 for success, _ in results.values() if success)
                total = len(results)
                print(f"📊 {module_name}: {successful}/{total}")
                
                # Zeige fehlgeschlagene Tests
                failed = [(name, msg) for name, (success, msg) in results.items() if not success]
                if failed:
                    for name, msg in failed:
                        print(f"   ❌ {name}: {msg[:80]}...")
        
        print(f"\n🎯 EMPFEHLUNGEN:")
        if total_successful == total_tests:
            print("✨ Alle Tests erfolgreich! API ist vollständig funktionsfähig.")
        elif total_successful > total_tests * 0.8:
            print("👍 Größtenteils funktionsfähig. Einzelne Endpunkte prüfen.")
        elif total_successful > total_tests * 0.5:
            print("⚠️  Mäßig funktionsfähig. Systematische Probleme möglich.")
        else:
            print("🚨 Viele Probleme gefunden. Grundlegende API-Probleme.")
        
        # Erstelle Report-Datei
        self.create_test_report(total_successful, total_tests, duration)
    
    def create_test_report(self, successful: int, total: int, duration: float):
        """Erstellt einen detaillierten Test-Report"""
        report_content = f"""# MCP DOCASSEMBLE API TEST REPORT
Datum: {time.strftime('%Y-%m-%d %H:%M:%S')}
Dauer: {duration:.1f} Sekunden
Server: http://192.168.178.29

## ZUSAMMENFASSUNG
- ✅ Erfolgreich: {successful}/{total} ({successful/total*100:.1f}%)
- ❌ Fehlgeschlagen: {total - successful}/{total}

## DETAILLIERTE ERGEBNISSE

"""
        
        for module_name, results in self.all_results.items():
            report_content += f"### {module_name}\n"
            
            if "error" in results:
                report_content += f"❌ MODUL-FEHLER: {results['error'][1]}\n\n"
            else:
                module_successful = sum(1 for success, _ in results.values() if success)
                module_total = len(results)
                report_content += f"Erfolg: {module_successful}/{module_total}\n\n"
                
                for endpoint, (success, message) in results.items():
                    status = "✅" if success else "❌"
                    report_content += f"- {status} `{endpoint}`: {message}\n"
                
                report_content += "\n"
        
        # Schreibe Report
        with open("TEST_REPORT.md", "w", encoding="utf-8") as f:
            f.write(report_content)
        
        print(f"📄 Detaillierter Report erstellt: TEST_REPORT.md")

if __name__ == "__main__":
    try:
        runner = MasterTestRunner()
        runner.run_all_tests()
    except KeyboardInterrupt:
        print("\n⚠️ Tests durch Benutzer abgebrochen")
    except Exception as e:
        print(f"\n🚨 KRITISCHER FEHLER: {e}")
        sys.exit(1)
