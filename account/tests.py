from django.test import TestCase
from django.contrib.auth import get_user_model
from account.models import EmailAccount

class EmailAccountModelTestCase(TestCase):
    def setUp(self):
        # Create a regular user
        self.user = get_user_model().objects.create_user(
            first_name='John',
            last_name='Doe',
            phone_number='1234567890',
            password='testpassword',
        )

        # Create an admin user with 'is_admin' set to True
        self.admin_user = get_user_model().objects.create_admin(
            phone_number='9876543210',
            password='adminpassword',
        )
        self.admin_user.is_admin = True  # Set the 'is_admin' attribute to True
        self.admin_user.save()

        # Create a staff user
        self.staff_user = get_user_model().objects.create_staff(
            phone_number='1111111111',
            password='staffpassword',
        )

    def test_has_perm_method(self):
        # Regular user should not have any permission
        self.assertFalse(self.user.has_perm('add'))
        self.assertFalse(self.user.has_perm('change'))
        self.assertFalse(self.user.has_perm('delete'))

        # Admin user should have 'add', 'change', and 'delete' permissions
        self.assertTrue(self.admin_user.has_perm('add'))
        self.assertTrue(self.admin_user.has_perm('change'))
        self.assertTrue(self.admin_user.has_perm('delete'))

        # Staff user should have 'add' and 'change' permissions, but not 'delete'
        self.assertTrue(self.staff_user.has_perm('add'))
        self.assertTrue(self.staff_user.has_perm('change'))
        self.assertFalse(self.staff_user.has_perm('delete'))

    def test_has_module_perms_method(self):
        # Regular user should not have any module-level permission
        self.assertFalse(self.user.has_module_perms('account'))

        # Admin user should have module-level permission for the 'account' app
        self.assertTrue(self.admin_user.has_module_perms('account'))

        # Staff user should have module-level permission for the 'account' app
        self.assertTrue(self.staff_user.has_module_perms('account'))
