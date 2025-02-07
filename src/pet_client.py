from src.base_api_client import BaseApiClient


class PetClient(BaseApiClient):

    
    def update_pet_image(self, pet_id, new_image):
        files = {"file": open(new_image , "rb")}
        return self.post(endpoint=f"/{pet_id}/uploadImage", files=files)
