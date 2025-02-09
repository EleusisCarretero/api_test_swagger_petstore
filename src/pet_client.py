"""
Petclient class file and relates
"""
from src.base_api_client import BaseApiClient


class PetClient(BaseApiClient):
    """
    Pet client class
    """
    def update_pet_image(self, pet_id, new_image=""):
        """
        Method to POST a give image to an specific petID

        Args:
            pet_id(str): PetID
            new_image(str): Path to the image
        """
        files = None
        if new_image:
            files = {"file": open(new_image , "rb")}
        return self.post(endpoint=f"/{pet_id}/uploadImage", files=files)
