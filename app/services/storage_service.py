"""Storage service for file operations using Supabase Storage."""

import os
import uuid
from typing import Optional, Tuple

from supabase import Client


class StorageService:
    """Service for handling file storage operations with Supabase."""

    def __init__(self, supabase: Client):
        self.supabase = supabase
        self.bucket_name = "task-attachments"

    def upload_file(
        self, 
        user_id: str, 
        file_content: bytes, 
        file_name: str,
        content_type: str = "application/octet-stream"
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Upload a file to Supabase Storage.
        
        Files are organized by user_id for RLS policies.
        
        Returns:
            Tuple of (success, message, file_path)
        """
        try:
            # Generate unique file name to avoid collisions
            file_extension = os.path.splitext(file_name)[1]
            unique_name = f"{uuid.uuid4().hex}{file_extension}"
            
            # Store files in user-specific folders for RLS
            file_path = f"{user_id}/{unique_name}"
            
            # Upload to Supabase Storage
            response = self.supabase.storage.from_(self.bucket_name).upload(
                path=file_path,
                file=file_content,
                file_options={"content-type": content_type}
            )
            
            return True, "File uploaded successfully", file_path
            
        except Exception as e:
            error_msg = str(e)
            # Handle common errors
            if "Bucket not found" in error_msg:
                return False, "Storage bucket not configured. Please create 'task-attachments' bucket in Supabase.", None
            return False, f"Error uploading file: {error_msg}", None

    def get_file_url(self, file_path: str, expires_in: int = 3600) -> Tuple[bool, str, Optional[str]]:
        """
        Get a signed URL for a file.
        
        Args:
            file_path: Path to the file in storage
            expires_in: URL expiration time in seconds (default 1 hour)
            
        Returns:
            Tuple of (success, message, signed_url)
        """
        try:
            response = self.supabase.storage.from_(self.bucket_name).create_signed_url(
                path=file_path,
                expires_in=expires_in
            )
            
            if response and "signedURL" in response:
                return True, "URL generated successfully", response["signedURL"]
            return False, "Failed to generate URL", None
            
        except Exception as e:
            return False, f"Error generating URL: {str(e)}", None

    def get_public_url(self, file_path: str) -> str:
        """
        Get a public URL for a file (only works for public buckets).
        
        Returns:
            Public URL string
        """
        return self.supabase.storage.from_(self.bucket_name).get_public_url(file_path)

    def delete_file(self, file_path: str) -> Tuple[bool, str]:
        """
        Delete a file from storage.
        
        Returns:
            Tuple of (success, message)
        """
        try:
            self.supabase.storage.from_(self.bucket_name).remove([file_path])
            return True, "File deleted successfully"
        except Exception as e:
            return False, f"Error deleting file: {str(e)}"

    def list_files(self, user_id: str) -> Tuple[bool, str, list]:
        """
        List all files for a user.
        
        Returns:
            Tuple of (success, message, files_list)
        """
        try:
            response = self.supabase.storage.from_(self.bucket_name).list(path=user_id)
            return True, "Files retrieved successfully", response or []
        except Exception as e:
            return False, f"Error listing files: {str(e)}", []

    def get_file_info(self, file_path: str) -> Optional[dict]:
        """
        Get file information including name and type.
        
        Returns:
            Dict with file info or None
        """
        if not file_path:
            return None
        
        parts = file_path.split("/")
        if len(parts) < 2:
            return None
        
        filename = parts[-1]
        extension = os.path.splitext(filename)[1].lower()
        
        # Determine file type for display
        image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"]
        pdf_extensions = [".pdf"]
        
        if extension in image_extensions:
            file_type = "image"
        elif extension in pdf_extensions:
            file_type = "pdf"
        else:
            file_type = "file"
        
        return {
            "path": file_path,
            "filename": filename,
            "extension": extension,
            "type": file_type,
        }

