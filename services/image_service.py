"""
=========================================
CivicPulse Image Service
=========================================

Handles image upload business logic.

Author : Sagar Sen
Project: CivicPulse
"""

import os

from flask import current_app

from models.complaint_image_model import ComplaintImageModel
from utils.file_utils import (
    allowed_file,
    generate_unique_filename
)


class ImageService:

    # ==========================================
    # Save Complaint Image
    # ==========================================

    @staticmethod
    def save_complaint_image(
        image,
        complaint_id
    ):
        """
        Validate, save, and store metadata
        for a citizen complaint image.
        """

        if image is None:

            return False, None, "No image selected."

        if not image.filename:

            return False, None, "Invalid image file."

        # --------------------------------------
        # Validate File Type
        # --------------------------------------

        if not allowed_file(image.filename):

            return (
                False,
                None,
                "File type is not allowed."
            )

        # --------------------------------------
        # Generate Unique Filename
        # --------------------------------------

        filename = generate_unique_filename(
            image.filename
        )

        # --------------------------------------
        # Upload Directory
        # --------------------------------------

        upload_folder = current_app.config.get(
            "COMPLAINT_IMAGE_FOLDER"
        )

        if not upload_folder:

            upload_folder = os.path.join(
                current_app.root_path,
                "static",
                "uploads",
                "complaint_images"
            )

        os.makedirs(
            upload_folder,
            exist_ok=True
        )

        # --------------------------------------
        # Save Physical File
        # --------------------------------------

        file_path = os.path.join(
            upload_folder,
            filename
        )

        try:

            image.save(file_path)

        except Exception as error:

            print(
                "❌ Image Save Error:",
                error
            )

            return (
                False,
                None,
                "Unable to save image."
            )

        # --------------------------------------
        # Store Relative Path
        # --------------------------------------

        relative_path = os.path.join(
            "uploads",
            "complaint_images",
            filename
        ).replace("\\", "/")

        # --------------------------------------
        # Save Metadata To Oracle
        # --------------------------------------

        success, message = ComplaintImageModel.create_image(

            complaint_id=complaint_id,

            image_path=relative_path,

            image_type="COMPLAINT"

        )

        if not success:

            # Remove physical file if database
            # metadata could not be saved.

            try:

                os.remove(file_path)

            except OSError:

                pass

            return (
                False,
                None,
                message
            )

        return (
            True,
            relative_path,
            "Complaint image uploaded successfully."
        )


    # ==========================================
    # Save Resolution Proof
    # ==========================================

    @staticmethod
    def save_resolution_proof(
        image,
        complaint_id
    ):
        """
        Save an image that will later be used
        as worker resolution proof.
        """

        if image is None or not image.filename:

            return False, None, "No image selected."

        if not allowed_file(image.filename):

            return (
                False,
                None,
                "File type is not allowed."
            )

        filename = generate_unique_filename(
            image.filename
        )

        upload_folder = current_app.config.get(
            "RESOLUTION_PROOF_FOLDER"
        )

        if not upload_folder:

            upload_folder = os.path.join(
                current_app.root_path,
                "static",
                "uploads",
                "resolution_proofs"
            )

        os.makedirs(
            upload_folder,
            exist_ok=True
        )

        file_path = os.path.join(
            upload_folder,
            filename
        )

        try:

            image.save(file_path)

        except Exception as error:

            print(
                "❌ Resolution Proof Save Error:",
                error
            )

            return (
                False,
                None,
                "Unable to save resolution proof."
            )

        relative_path = os.path.join(
            "uploads",
            "resolution_proofs",
            filename
        ).replace("\\", "/")

        success, message = ComplaintImageModel.create_image(

            complaint_id=complaint_id,

            image_path=relative_path,

            image_type="RESOLUTION"

        )

        if not success:

            try:

                os.remove(file_path)

            except OSError:

                pass

            return (
                False,
                None,
                message
            )

        return (
            True,
            relative_path,
            "Resolution proof uploaded successfully."
        )