"""
Test Modul: Benutzer-Management API Endpunkte
Tests für alle benutzer-bezogenen Endpunkte
"""

import time
from typing import Dict, Tuple

from .test_base import APITestBase


class UserManagementTests(APITestBase):
    """Tests für Benutzer-Management Endpunkte"""

    def run_all_tests(self) -> Dict[str, Tuple[bool, str]]:
        """Führt alle Benutzer-Management Tests aus"""
        self.print_section_header("BENUTZER-MANAGEMENT TESTS", 12)

        results = {}

        # Basis-Benutzer Tests
        results["create_user"] = self.test_endpoint(
            "create_user", self._test_create_user
        )

        results["invite_users"] = self.test_endpoint(
            "invite_users", self._test_invite_users
        )

        results["list_users"] = self.test_endpoint("list_users", self._test_list_users)

        results["get_user_by_username"] = self.test_endpoint(
            "get_user_by_username", self._test_get_user_by_username
        )

        results["get_current_user"] = self.test_endpoint(
            "get_current_user", self._test_get_current_user
        )

        results["update_current_user"] = self.test_endpoint(
            "update_current_user", self._test_update_current_user
        )

        results["get_user_by_id"] = self.test_endpoint(
            "get_user_by_id", self._test_get_user_by_id
        )

        results["deactivate_user"] = self.test_endpoint(
            "deactivate_user", self._test_deactivate_user
        )

        results["update_user"] = self.test_endpoint(
            "update_user", self._test_update_user
        )

        # Rechte-Management Tests
        results["list_privileges"] = self.test_endpoint(
            "list_privileges", self._test_list_privileges
        )

        results["give_user_privilege"] = self.test_endpoint(
            "give_user_privilege", self._test_give_user_privilege
        )

        results["remove_user_privilege"] = self.test_endpoint(
            "remove_user_privilege", self._test_remove_user_privilege
        )

        self.print_results(results)
        return results

    def _test_create_user(self):
        """Test: Benutzer erstellen"""
        return self.client.create_user(
            username=f"testuser_{int(time.time())}@example.com",
            password="TestPassword123!",
            first_name="Test",
            last_name="User",
        )

    def _test_invite_users(self):
        """Test: Benutzer einladen"""
        return self.client.invite_users(
            email_addresses=[f"invited_{int(time.time())}@example.com"],
            privilege="user",
            send_emails=False,
        )

    def _test_list_users(self):
        """Test: Benutzer auflisten"""
        return self.client.list_users(include_inactive=False)

    def _test_get_user_by_username(self):
        """Test: Benutzer per Username holen"""
        return self.client.get_user_by_username(username="admin@example.com")

    def _test_get_current_user(self):
        """Test: Aktuellen Benutzer holen"""
        return self.client.get_current_user()

    def _test_update_current_user(self):
        """Test: Aktuellen Benutzer aktualisieren"""
        return self.client.update_current_user(first_name="Updated")

    def _test_get_user_by_id(self):
        """Test: Benutzer per ID holen"""
        return self.client.get_user_by_id(user_id=1)  # Admin User

    def _test_deactivate_user(self):
        """Test: Benutzer deaktivieren"""
        # Erstelle erst einen Test-User zum Deaktivieren
        user_result = self.client.create_user(
            username=f"todelete_{int(time.time())}@example.com",
            password="TestPassword123!",
        )
        user_id = user_result["user_id"]
        return self.client.deactivate_user(user_id=user_id)

    def _test_update_user(self):
        """Test: Benutzer aktualisieren"""
        return self.client.update_user(user_id=1, first_name="UpdatedAdmin")

    def _test_list_privileges(self):
        """Test: Privilegien auflisten"""
        return self.client.list_privileges()

    def _test_give_user_privilege(self):
        """Test: Benutzer Privileg geben"""
        # Finde einen Test-User ohne Admin-Rechte
        users = self.client.list_users()
        test_user = next(
            (
                u
                for u in users["items"]
                if "admin" not in u["privileges"] and u["id"] != 1
            ),
            None,
        )
        if test_user:
            return self.client.give_user_privilege(
                user_id=test_user["id"], privilege="advocate"
            )
        else:
            return {"message": "Kein geeigneter Test-User gefunden"}

    def _test_remove_user_privilege(self):
        """Test: Benutzer Privileg entziehen"""
        # Finde einen Test-User mit Rechten
        users = self.client.list_users()
        test_user = next(
            (u for u in users["items"] if len(u["privileges"]) > 0 and u["id"] != 1),
            None,
        )
        if test_user and test_user["privileges"]:
            return self.client.remove_user_privilege(
                user_id=test_user["id"], privilege=test_user["privileges"][0]
            )
        else:
            return {"message": "Kein geeigneter Test-User mit Rechten gefunden"}
