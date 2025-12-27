"""Authentication service using Supabase Auth."""

from typing import Optional, Tuple

from supabase import Client

# Import AuthApiError from the correct location in supabase-py
try:
    from gotrue.errors import AuthApiError
except ImportError:
    # Fallback for different versions of supabase-py
    AuthApiError = Exception


class AuthService:
    """Service for handling authentication operations with Supabase."""

    def __init__(self, supabase: Client):
        self.supabase = supabase

    def sign_up(self, email: str, password: str) -> Tuple[bool, str, Optional[dict]]:
        """
        Register a new user.
        
        Returns:
            Tuple of (success, message, user_data)
        """
        try:
            response = self.supabase.auth.sign_up({
                "email": email,
                "password": password,
            })
            
            if response.user:
                return True, "Registration successful! Please check your email to confirm.", {
                    "id": response.user.id,
                    "email": response.user.email,
                }
            else:
                return False, "Registration failed. Please try again.", None
                
        except AuthApiError as e:
            return False, str(e.message), None
        except Exception as e:
            return False, f"An error occurred: {str(e)}", None

    def sign_in(self, email: str, password: str) -> Tuple[bool, str, Optional[dict]]:
        """
        Sign in an existing user.
        
        Returns:
            Tuple of (success, message, session_data)
        """
        try:
            response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password,
            })
            
            if response.user and response.session:
                return True, "Login successful!", {
                    "user": {
                        "id": response.user.id,
                        "email": response.user.email,
                    },
                    "access_token": response.session.access_token,
                    "refresh_token": response.session.refresh_token,
                }
            else:
                return False, "Login failed. Please check your credentials.", None
                
        except AuthApiError as e:
            return False, str(e.message), None
        except Exception as e:
            return False, f"An error occurred: {str(e)}", None

    def sign_out(self, access_token: Optional[str] = None) -> Tuple[bool, str]:
        """
        Sign out the current user.
        
        Returns:
            Tuple of (success, message)
        """
        try:
            self.supabase.auth.sign_out()
            return True, "Logged out successfully."
        except Exception as e:
            return False, f"Error signing out: {str(e)}"

    def get_user_from_token(self, access_token: str) -> Optional[dict]:
        """
        Get user information from an access token.
        
        Returns:
            User dict if valid, None otherwise
        """
        try:
            response = self.supabase.auth.get_user(access_token)
            if response.user:
                return {
                    "id": response.user.id,
                    "email": response.user.email,
                }
            return None
        except Exception:
            return None

    def refresh_session(self, refresh_token: str) -> Tuple[bool, Optional[dict]]:
        """
        Refresh an expired session using a refresh token.
        
        Returns:
            Tuple of (success, new_session_data)
        """
        try:
            response = self.supabase.auth.refresh_session(refresh_token)
            if response.session:
                return True, {
                    "access_token": response.session.access_token,
                    "refresh_token": response.session.refresh_token,
                }
            return False, None
        except Exception:
            return False, None

