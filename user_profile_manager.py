import asyncio
from external_validation_service import ExternalValidationService


class UserProfileManager:
    def __init__(self):
        self.user_profiles = {}
        self.external_validation_service = ExternalValidationService()

    async def add_user(self, user_id, user_info):
        if user_id in self.user_profiles:
            raise ValueError("User already exists")
        validation_result = await self.external_validation_service.validate(user_info)
        if not validation_result:
            raise ValueError("User info validation failed")
        self.user_profiles[user_id] = user_info
        return "User added successfully"

    def update_user(self, user_id, user_info):
        if user_id not in self.user_profiles:
            raise KeyError("User does not exist")
        self.user_profiles[user_id] = user_info
        return "User updated successfully"

    def delete_user(self, user_id):
        if user_id not in self.user_profiles:
            raise KeyError("User does not exist")
        del self.user_profiles[user_id]
        return "User deleted successfully"

    async def merge_user_profiles(self, primary_user_id, secondary_user_id):
        if primary_user_id not in self.user_profiles or secondary_user_id not in self.user_profiles:
            raise KeyError("One or both users do not exist")
        primary_profile = self.user_profiles[primary_user_id]
        secondary_profile = self.user_profiles[secondary_user_id]
        merged_profile = {**secondary_profile, **primary_profile}  # Simplified merge strategy
        self.user_profiles[primary_user_id] = merged_profile
        del self.user_profiles[secondary_user_id]
        return "Profiles merged successfully"