"""
Enhanced Docassemble Client Extensions

Verbesserungen für:
1. Session-Timeout-Konfiguration
2. Version-Detection
3. Graceful Fallbacks
4. Robustes Error Handling
"""

import json
import logging
import re
import time
from typing import Any, Dict, List, Optional, Union

from requests.exceptions import RequestException, Timeout

logger = logging.getLogger(__name__)


class DocassembleAPIError(Exception):
    """Docassemble API Error"""

    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class DocassembleClientEnhanced:
    """Enhanced mixin for DocassembleClient with improved capabilities."""

    def __init__(self, *args, **kwargs):
        # Extract enhancement parameters
        self.session_timeout = kwargs.pop("session_timeout", 3600)
        self.enable_fallbacks = kwargs.pop("enable_fallbacks", True)
        self.auto_retry = kwargs.pop("auto_retry", True)

        super().__init__(*args, **kwargs)

        # Initialize enhanced features
        self.da_version = self._detect_docassemble_version()
        self._init_feature_compatibility()

    def _detect_docassemble_version(self) -> Optional[str]:
        """Detect Docassemble version and capabilities."""
        try:
            # Try to get server configuration which usually contains version info
            config = self.get_server_config()
            if config and isinstance(config, dict):
                # Look for version indicators
                version = (
                    config.get("version")
                    or config.get("build")
                    or config.get("da_version")
                )
                if version:
                    logger.info(f"Detected Docassemble version: {version}")
                    return str(version)
        except Exception as e:
            logger.debug(f"Could not detect version via config: {e}")

        try:
            # Fallback: try to detect through available endpoints
            response = self.session.get(f"{self.base_url}/", timeout=5)
            if "Docassemble" in response.text:
                # Parse version from HTML if available
                import re

                version_match = re.search(
                    r'Docassemble[^0-9]*([0-9]+\.[0-9]+[^"<\s]*)', response.text
                )
                if version_match:
                    version = version_match.group(1)
                    logger.info(f"Detected Docassemble version from HTML: {version}")
                    return version
        except Exception as e:
            logger.debug(f"Could not detect version via HTML: {e}")

        logger.warning(
            "Could not detect Docassemble version, using default compatibility"
        )
        return "unknown"

    def _init_feature_compatibility(self):
        """Initialize feature compatibility matrix based on version."""
        self.feature_support = {
            # File operations - often problematic
            "convert_file_to_markdown": False,
            "extract_template_fields": True,  # Usually works with proper file upload
            "retrieve_stored_file": False,
            # URL generation - version dependent
            "get_redirect_url": False,
            "get_login_url": False,
            # Playground operations - often restricted
            "pull_package_to_playground": False,
            "create_playground_project": True,  # Works with proper naming
            # Session management - available but needs careful handling
            "advanced_session_management": True,
            "session_variables": True,
            # Package management - usually available
            "install_or_update_package": True,
            "package_management": True,
        }

        # Adjust based on detected version
        if self.da_version and self.da_version != "unknown":
            try:
                # Parse version and adjust features
                version_parts = self.da_version.replace("v", "").split(".")
                major = int(version_parts[0]) if version_parts else 0

                # Enable more features for newer versions
                if major >= 1:  # Assuming version 1.x and above
                    self.feature_support.update(
                        {
                            "convert_file_to_markdown": True,
                            "get_redirect_url": True,
                        }
                    )

                logger.info(f"Configured features for version {self.da_version}")
            except Exception as e:
                logger.debug(f"Could not parse version for feature detection: {e}")

    def _is_feature_supported(self, feature: str) -> bool:
        """Check if a feature is supported in current version."""
        return self.feature_support.get(feature, True)

    def _graceful_fallback(
        self, feature_name: str, fallback_result: Any = None, error_message: str = None
    ):
        """Provide graceful fallback for unsupported features."""
        if not self.enable_fallbacks:
            raise DocassembleAPIError(
                error_message
                or f"Feature '{feature_name}' not supported in this Docassemble version"
            )

        logger.warning(f"Feature '{feature_name}' not available, using fallback")

        if fallback_result is not None:
            return fallback_result

        return {
            "status": "unsupported",
            "feature": feature_name,
            "message": error_message or "Feature not available in this version",
            "version": self.da_version,
            "fallback": True,
        }

    def _enhanced_request(self, method: str, endpoint: str, **kwargs):
        """Enhanced request with retry logic and better error handling."""
        try:
            return self._request(method, endpoint, **kwargs)
        except DocassembleAPIError as e:
            # Check for specific error patterns and provide fallbacks
            if e.status_code == 404 and "HTML_ERROR_PAGE" in str(e.response_data):
                feature_name = endpoint.split("/")[-1]
                if self.enable_fallbacks:
                    return self._graceful_fallback(
                        feature_name,
                        error_message=f"API endpoint '{endpoint}' not available in this version",
                    )

            # Auto-retry for certain error types
            if self.auto_retry and e.status_code in [500, 502, 503, 504]:
                logger.warning(f"Retrying request to {endpoint} after error: {e}")
                try:
                    import time

                    time.sleep(1)  # Brief pause before retry
                    return self._request(method, endpoint, **kwargs)
                except Exception:
                    pass  # Fall through to original error

            raise

    def enhanced_start_interview(self, i: str, **kwargs) -> Dict[str, Any]:
        """Enhanced interview start with session timeout configuration."""
        try:
            result = self.start_interview(i, **kwargs)

            # Add session management metadata
            if isinstance(result, dict) and "session" in result:
                result.update(
                    {
                        "session_timeout": self.session_timeout,
                        "client_version": getattr(self, "__version__", "unknown"),
                        "da_version": self.da_version,
                        "enhanced": True,
                    }
                )

            return result
        except Exception as e:
            logger.error(f"Enhanced interview start failed: {e}")
            if self.enable_fallbacks:
                return self._graceful_fallback(
                    "start_interview",
                    error_message=f"Could not start interview '{i}': {str(e)}",
                )
            raise

    def enhanced_get_interview_variables(self, session: str, i: str, **kwargs):
        """Enhanced variable retrieval with session validation."""
        if not self._is_feature_supported("session_variables"):
            return self._graceful_fallback("get_interview_variables")

        try:
            return self.get_interview_variables(session, i, **kwargs)
        except DocassembleAPIError as e:
            if "Unable to obtain interview" in str(e):
                if self.enable_fallbacks:
                    logger.warning(
                        f"Session {session} expired or invalid, providing fallback"
                    )
                    return {
                        "variables": {},
                        "status": "session_expired",
                        "message": "Session expired or invalid",
                        "session": session,
                        "fallback": True,
                    }
            raise

    def get_version_info(self) -> Dict[str, Any]:
        """Get comprehensive version and capability information."""
        return {
            "docassemble_version": self.da_version,
            "client_version": getattr(self, "__version__", "unknown"),
            "features_supported": self.feature_support,
            "fallbacks_enabled": self.enable_fallbacks,
            "session_timeout": self.session_timeout,
            "base_url": self.base_url,
        }
