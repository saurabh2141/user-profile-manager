import unittest
from unittest.mock import AsyncMock, patch
from user_profile_manager import UserProfileManager  # Replace 'your_module' with the actual module name

class TestUserProfileManager(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.manager = UserProfileManager()

    @patch("user_profile_manager.ExternalValidationService.validate", new_callable=AsyncMock)  # Replace 'your_module'
    async def test_add_user_success(self, mock_validate):
        mock_validate.return_value = True
        user_info = {"name": "Test User", "email": "test@example.com"}
        result = await self.manager.add_user(1, user_info)
        self.assertEqual(result, "User added successfully")
        self.assertEqual(self.manager.user_profiles[1], user_info)
        mock_validate.assert_awaited_once_with(user_info)

    async def test_add_user_already_exists(self):
        self.manager.user_profiles[1] = {}
        with self.assertRaises(ValueError) as cm:
            await self.manager.add_user(1, {})
        self.assertEqual(str(cm.exception), "User already exists")

    @patch("user_profile_manager.ExternalValidationService.validate", new_callable=AsyncMock)  # Replace 'your_module'
    async def test_add_user_validation_fails(self, mock_validate):
        mock_validate.return_value = False
        with self.assertRaises(ValueError) as cm:
            await self.manager.add_user(1, {})
        self.assertEqual(str(cm.exception), "User info validation failed")

    def test_update_user_success(self):
        self.manager.user_profiles[1] = {"name": "Old Name"}
        new_info = {"name": "New Name", "email": "test@example.com"}
        result = self.manager.update_user(1, new_info)
        self.assertEqual(result, "User updated successfully")
        self.assertEqual(self.manager.user_profiles[1], new_info)

    def test_update_user_not_found(self):
        with self.assertRaises(KeyError) as cm:
            self.manager.update_user(1, {})
        self.assertEqual(str(cm.exception), "User does not exist")

    def test_delete_user_success(self):
        self.manager.user_profiles[1] = {}
        result = self.manager.delete_user(1)
        self.assertEqual(result, "User deleted successfully")
        self.assertNotIn(1, self.manager.user_profiles)

    def test_delete_user_not_found(self):
        with self.assertRaises(KeyError) as cm:
            self.manager.delete_user(1)
        self.assertEqual(str(cm.exception), "User does not exist")

    async def test_merge_user_profiles_success(self):
        self.manager.user_profiles[1] = {"name": "User 1", "email": "user1@example.com"}
        self.manager.user_profiles[2] = {"age": 30, "location": "City"}
        result = await self.manager.merge_user_profiles(1, 2)
        self.assertEqual(result, "Profiles merged successfully")
        expected_merged_profile = {
            "name": "User 1", "email": "user1@example.com", "age": 30, "location": "City"
        }
        self.assertEqual(self.manager.user_profiles[1], expected_merged_profile)
        self.assertNotIn(2, self.manager.user_profiles)

    async def test_merge_user_profiles_one_user_not_found(self):
        self.manager.user_profiles[1] = {}
        with self.assertRaises(KeyError) as cm:
            await self.manager.merge_user_profiles(1, 2)
        self.assertEqual(str(cm.exception), "One or both users do not exist")

    async def test_merge_user_profiles_both_users_not_found(self):
        with self.assertRaises(KeyError) as cm:
            await self.manager.merge_user_profiles(1, 2)
        self.assertEqual(str(cm.exception), "One or both users do not exist")

if __name__ == "__main__":
    unittest.main()