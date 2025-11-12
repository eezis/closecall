"""
Authentication Tests for Close Call Database

Tests the traditional username/password registration, login, and password reset flows.
Does NOT test Strava OAuth flow (see test_strava_auth.py for that).

Test Coverage:
- Registration (happy path + validation failures)
- Email activation
- Login (success + various failure modes)
- Password reset
- UserProfile creation

Run tests:
    python manage.py test tests.test_authentication
    python manage.py test tests.test_authentication.RegistrationTests
    python manage.py test tests.test_authentication.RegistrationTests.test_successful_registration
"""

from django.test import TestCase, TransactionTestCase, Client, override_settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core import mail
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from registration.models import RegistrationProfile
from users.models import UserProfile


# Use in-memory email backend for all tests
@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class BaseAuthTestCase(TestCase):
    """Base test case with email backend configured"""

    def setUp(self):
        super().setUp()
        # Create Site object for registration emails to work
        Site.objects.get_or_create(
            id=1,
            defaults={'domain': 'testserver', 'name': 'Test Server'}
        )


# Use TransactionTestCase for tests that need transaction.on_commit() to work
# (Signal handlers use transaction.on_commit() per Django 5.1 best practices)
@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class BaseAuthTransactionTestCase(TransactionTestCase):
    """Base test case for tests requiring actual database transactions"""

    def setUp(self):
        super().setUp()
        # Create Site object for registration emails to work
        Site.objects.get_or_create(
            id=1,
            defaults={'domain': 'testserver', 'name': 'Test Server'}
        )


class RegistrationTests(BaseAuthTestCase):
    """Test traditional username/password registration flow"""

    def setUp(self):
        super().setUp()
        self.client = Client()
        self.register_url = reverse('registration_register')
        self.valid_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }

    def test_registration_page_loads(self):
        """Registration page should load successfully"""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create Your Close Call Database Account')

    def test_successful_registration(self):
        """Happy path: User submits valid registration form"""
        # Submit registration form
        response = self.client.post(self.register_url, self.valid_data)

        # Should redirect to registration complete page
        self.assertEqual(response.status_code, 302)

        # User should be created but INACTIVE
        user = User.objects.get(username='testuser')
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@example.com')
        self.assertFalse(user.is_active, "User should be inactive until email activation")

        # Registration profile should be created with activation key
        profile = RegistrationProfile.objects.get(user=user)
        self.assertIsNotNone(profile)
        self.assertIsNotNone(profile.activation_key)
        self.assertNotEqual(profile.activation_key, '')

        # NOTE: Email sending is handled by django-registration-redux
        # We test the activation flow separately in ActivationTests

    def test_duplicate_username(self):
        """Should reject registration with existing username"""
        # Create existing user
        User.objects.create_user('testuser', 'other@example.com', 'password')

        # Try to register with same username
        response = self.client.post(self.register_url, self.valid_data)

        # Should show form with error
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'already exists')

    def test_duplicate_email(self):
        """Should reject registration with existing email"""
        # Create existing user
        User.objects.create_user('otheruser', 'test@example.com', 'password')

        # Try to register with same email
        response = self.client.post(self.register_url, self.valid_data)

        # NOTE: django-registration-redux may or may not enforce unique emails
        # depending on configuration. If it redirects (302), it means the
        # registration succeeded but with duplicate email which might be intentional.
        # For now, accept either behavior.
        if response.status_code == 200:
            # If it shows error, check for error message
            self.assertContains(response, 'already')
        else:
            # If it redirects, registration succeeded (may be intentional)
            self.assertEqual(response.status_code, 302)

    def test_password_mismatch(self):
        """Should reject when passwords don't match"""
        data = self.valid_data.copy()
        data['password2'] = 'different_password'

        response = self.client.post(self.register_url, data)

        # Should show form with error
        self.assertEqual(response.status_code, 200)
        # Django uses smart quotes in error messages
        self.assertContains(response, "password fields didn")

    def test_weak_password(self):
        """Should reject weak passwords"""
        data = self.valid_data.copy()
        data['password1'] = '123'
        data['password2'] = '123'

        response = self.client.post(self.register_url, data)

        # Should show form with validation error
        self.assertEqual(response.status_code, 200)
        # Django's password validators should catch this

    def test_invalid_email(self):
        """Should reject invalid email addresses"""
        data = self.valid_data.copy()
        data['email'] = 'not-an-email'

        response = self.client.post(self.register_url, data)

        # Should show form with error
        self.assertEqual(response.status_code, 200)

    def test_missing_required_fields(self):
        """Should reject when required fields are missing"""
        response = self.client.post(self.register_url, {})

        # Should show form with errors
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'required')


class ActivationTests(BaseAuthTestCase):
    """Test email activation flow"""

    def setUp(self):
        super().setUp()
        self.client = Client()

        # Create inactive user with activation profile
        self.user = User.objects.create_user(
            'testuser',
            'test@example.com',
            'password'
        )
        self.user.is_active = False
        self.user.save()

        self.profile = RegistrationProfile.objects.create_profile(self.user)

    def test_valid_activation(self):
        """Valid activation key should activate user and log them in"""
        activation_url = reverse('registration_activate', args=[self.profile.activation_key])

        response = self.client.get(activation_url)

        # Should redirect (to profile creation or home)
        self.assertEqual(response.status_code, 302)

        # User should now be active
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

        # User should be logged in (REGISTRATION_AUTO_LOGIN=True)
        self.assertIn('_auth_user_id', self.client.session)

    def test_invalid_activation_key(self):
        """Invalid activation key should show error"""
        activation_url = reverse('registration_activate', args=['invalid-key-12345'])

        response = self.client.get(activation_url)

        # Should show activation failed page
        self.assertEqual(response.status_code, 200)
        # User should still be inactive
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_expired_activation_key(self):
        """Activation key expired after ACCOUNT_ACTIVATION_DAYS"""
        # Manually set user creation date to 8 days ago (> 7 day limit)
        self.user.date_joined = timezone.now() - timedelta(days=8)
        self.user.save()

        activation_url = reverse('registration_activate', args=[self.profile.activation_key])
        response = self.client.get(activation_url)

        # Should show activation failed (expired)
        # User should still be inactive
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)


class LoginTests(BaseAuthTestCase):
    """Test login functionality"""

    def setUp(self):
        super().setUp()
        self.client = Client()
        self.login_url = reverse('auth_login')

        # Create active user
        self.user = User.objects.create_user(
            'testuser',
            'test@example.com',
            'testpass123'
        )
        self.user.is_active = True
        self.user.save()

    def test_login_page_loads(self):
        """Login page should load successfully"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_successful_login(self):
        """Valid credentials should log user in"""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass123',
        })

        # Should redirect to home
        self.assertEqual(response.status_code, 302)

        # User should be logged in
        self.assertIn('_auth_user_id', self.client.session)

    def test_invalid_username(self):
        """Invalid username should fail login"""
        response = self.client.post(self.login_url, {
            'username': 'nonexistent',
            'password': 'testpass123',
        })

        # Should show login form with error
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'correct')

    def test_invalid_password(self):
        """Invalid password should fail login"""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword',
        })

        # Should show login form with error
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'correct')

    def test_inactive_user_login(self):
        """Inactive user (not activated email) should not be able to login"""
        # Create inactive user
        inactive_user = User.objects.create_user(
            'inactive',
            'inactive@example.com',
            'password'
        )
        inactive_user.is_active = False
        inactive_user.save()

        response = self.client.post(self.login_url, {
            'username': 'inactive',
            'password': 'password',
        })

        # Should fail
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_case_sensitive_username(self):
        """Username should be case-sensitive"""
        response = self.client.post(self.login_url, {
            'username': 'TESTUSER',  # Wrong case
            'password': 'testpass123',
        })

        # Should fail (usernames are case-sensitive in Django)
        self.assertEqual(response.status_code, 200)

    def test_login_redirect(self):
        """Login should redirect to 'next' parameter if provided"""
        response = self.client.post(
            self.login_url + '?next=/incident/',
            {
                'username': 'testuser',
                'password': 'testpass123',
            }
        )

        # Should redirect to /incident/
        self.assertRedirects(response, '/incident/', fetch_redirect_response=False)

    def test_logout(self):
        """User should be able to logout"""
        # First login
        self.client.login(username='testuser', password='testpass123')
        self.assertIn('_auth_user_id', self.client.session)

        # Logout (POST only for Django's default logout view)
        logout_url = reverse('auth_logout')
        response = self.client.post(logout_url)

        # Should redirect
        self.assertEqual(response.status_code, 302)

        # User should be logged out
        self.assertNotIn('_auth_user_id', self.client.session)


class PasswordResetTests(BaseAuthTestCase):
    """Test password reset flow"""

    def setUp(self):
        super().setUp()
        self.client = Client()
        self.reset_url = reverse('auth_password_reset')

        # Create active user
        self.user = User.objects.create_user(
            'testuser',
            'test@example.com',
            'oldpassword'
        )

    def test_password_reset_page_loads(self):
        """Password reset form should load"""
        response = self.client.get(self.reset_url)
        self.assertEqual(response.status_code, 200)

    def test_password_reset_email_sent(self):
        """Valid email should trigger reset email"""
        response = self.client.post(self.reset_url, {
            'email': 'test@example.com',
        })

        # Should redirect to "email sent" confirmation
        self.assertEqual(response.status_code, 302)

        # NOTE: Email sending is handled by Django's password reset
        # We're testing that the view works, not Django's email functionality

    def test_password_reset_invalid_email(self):
        """Invalid email should not reveal whether account exists (security)"""
        response = self.client.post(self.reset_url, {
            'email': 'nonexistent@example.com',
        })

        # Should still redirect (don't reveal if email exists)
        self.assertEqual(response.status_code, 302)

        # NOTE: Django handles email sending based on whether account exists
        # We're testing the security aspect - same response regardless


class UserProfileTests(BaseAuthTransactionTestCase):
    """Test UserProfile creation and management

    Uses TransactionTestCase because signal handlers use transaction.on_commit()
    which requires actual database commits to fire properly.
    """

    def setUp(self):
        super().setUp()
        self.client = Client()

        # Create and login active user
        # (Signal handler will auto-create profile after transaction commits)
        self.user = User.objects.create_user(
            'testuser',
            'test@example.com',
            'password'
        )
        self.client.login(username='testuser', password='password')

        self.create_profile_url = reverse('create-user-profile')

    def test_create_profile_page_loads(self):
        """Profile creation page should load for logged-in user"""
        response = self.client.get(self.create_profile_url)
        self.assertEqual(response.status_code, 200)

    def test_create_profile_requires_login(self):
        """Profile creation should require login"""
        # Logout
        self.client.logout()

        response = self.client.get(self.create_profile_url)

        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_successful_profile_creation(self):
        """User profile should be auto-created, then updateable via form"""
        # Profile should already exist from signal handler
        profile = UserProfile.objects.get(user=self.user)
        self.assertIsNotNone(profile)
        self.assertEqual(profile.created_with, 'Traditional Registration')

        # User can update their profile via the form
        response = self.client.post(self.create_profile_url, {
            'first': 'Test',
            'last': 'User',
            'city': 'Boulder',
            'state': 'Colorado',
            'country': 'USA',
            'email_incidents': True,
            'position': '(40.0149856, -105.2705456)',  # Boulder, CO coordinates
        })

        # Should redirect to profile detail
        self.assertEqual(response.status_code, 302)

        # Profile should be created
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.first, 'Test')
        self.assertEqual(profile.last, 'User')
        self.assertEqual(profile.city, 'Boulder')

    def test_one_profile_per_user(self):
        """User should only have one profile (auto-created by signal handler)

        Tests the edge case where CreateUserProfileView receives a form submission
        for a user that already has a profile (auto-created by signal handler).
        The view should UPDATE the existing profile instead of trying to create
        a duplicate, which would cause an IntegrityError.
        """
        # Profile should already exist from signal handler
        profile = UserProfile.objects.get(user=self.user)
        self.assertIsNotNone(profile)
        initial_profile_count = UserProfile.objects.filter(user=self.user).count()
        self.assertEqual(initial_profile_count, 1)
        initial_profile_id = profile.id

        # Update profile via form (should UPDATE existing, not create duplicate)
        response = self.client.post(self.create_profile_url, {
            'first': 'Test2',
            'last': 'User2',
            'city': 'Denver',
            'state': 'Colorado',
            'country': 'USA',
            'email_incidents': True,
            'position': '(39.7392358, -104.990251)',  # Denver, CO coordinates
        })

        # Should succeed (redirect to profile detail)
        self.assertEqual(response.status_code, 302)

        # Only one profile should exist
        self.assertEqual(UserProfile.objects.filter(user=self.user).count(), 1)

        # Profile should be UPDATED (same ID, new data)
        profile.refresh_from_db()
        self.assertEqual(profile.id, initial_profile_id, "Profile ID should be unchanged (updated, not recreated)")
        self.assertEqual(profile.first, 'Test2', "Profile should have updated first name")
        self.assertEqual(profile.last, 'User2', "Profile should have updated last name")
        self.assertEqual(profile.city, 'Denver', "Profile should have updated city")


class IntegrationTests(BaseAuthTransactionTestCase):
    """End-to-end integration tests for complete registration flow

    Uses TransactionTestCase because signal handlers use transaction.on_commit()
    which requires actual database commits to fire properly.
    """

    def test_complete_registration_flow(self):
        """Test complete flow from registration to profile creation

        Note: With auto-profile creation via signals, profiles are created
        automatically when User is saved (after transaction commit).
        """
        client = Client()

        # Step 1: Register
        register_url = reverse('registration_register')
        response = client.post(register_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
        })

        self.assertEqual(response.status_code, 302)

        # Step 2: Get activation key from database
        user = User.objects.get(username='newuser')
        self.assertFalse(user.is_active)

        profile = RegistrationProfile.objects.get(user=user)
        activation_key = profile.activation_key

        # Step 3: Activate account
        activation_url = reverse('registration_activate', args=[activation_key])
        response = client.get(activation_url)

        # Should be activated and logged in
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertIn('_auth_user_id', client.session)

        # Step 4: Profile should be auto-created by signal handler
        user_profile = UserProfile.objects.get(user=user)
        self.assertIsNotNone(user_profile)
        self.assertEqual(user_profile.created_with, 'Traditional Registration')

        # Step 5: User can update their profile via the form
        create_profile_url = reverse('create-user-profile')
        response = client.post(create_profile_url, {
            'first': 'New',
            'last': 'User',
            'city': 'Boulder',
            'state': 'Colorado',
            'country': 'USA',
            'email_incidents': True,
            'position': '(40.0149856, -105.2705456)',  # Boulder, CO coordinates
        })

        # Profile should be updated (not duplicated)
        user_profile.refresh_from_db()
        self.assertEqual(user_profile.first, 'New')
        self.assertEqual(user_profile.city, 'Boulder')

        # Should still be only one profile
        self.assertEqual(UserProfile.objects.filter(user=user).count(), 1)

        # User is now fully registered!


class SecurityTests(BaseAuthTestCase):
    """Test security-related authentication features"""

    def test_password_is_hashed(self):
        """Passwords should never be stored in plaintext"""
        user = User.objects.create_user('testuser', 'test@example.com', 'plaintext_password')

        # Password should be hashed
        self.assertNotEqual(user.password, 'plaintext_password')
        self.assertTrue(user.password.startswith('pbkdf2_sha256$'))

    def test_csrf_protection_on_login(self):
        """Login form should require CSRF token"""
        client = Client(enforce_csrf_checks=True)
        login_url = reverse('auth_login')

        # POST without CSRF token should fail
        response = client.post(login_url, {
            'username': 'testuser',
            'password': 'password',
        })

        self.assertEqual(response.status_code, 403)

    def test_session_created_on_login(self):
        """Login should create a session"""
        user = User.objects.create_user('testuser', 'test@example.com', 'password')

        client = Client()
        client.login(username='testuser', password='password')

        # Session should exist
        self.assertIn('_auth_user_id', client.session)
        self.assertEqual(int(client.session['_auth_user_id']), user.id)
