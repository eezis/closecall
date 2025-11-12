You're actually very well positioned for this! Your current architecture sets you up nicely. Here's what you
  already have vs. what you'd need:

  ✅ What You Already Have

  1. Location-based notification logic - utils/send_incident_emails.py already:
    - Finds users within radius of incident
    - Filters by user preferences (email_incidents)
    - Calculates distances
  2. REST API infrastructure - You have Django REST Framework installed with API endpoints
  3. User authentication system - Django auth + Strava OAuth
  4. Geocoded user locations - Position data already stored and validated
  5. Incident data model - Everything needed for notifications

  🔧 What You'd Need to Add

  1. Device Token Storage (users/models.py)

  class UserProfile(BaseFields):
      # ... existing fields ...

      # Push notification settings
      fcm_token = models.CharField(max_length=255, null=True, blank=True)
      apns_token = models.CharField(max_length=255, null=True, blank=True)
      push_enabled = models.BooleanField(default=True)
      last_token_update = models.DateTimeField(null=True, blank=True)

  2. Firebase Cloud Messaging (FCM)

  uv pip install firebase-admin

  3. Push Notification Service (utils/send_push_notifications.py)

  import firebase_admin
  from firebase_admin import credentials, messaging

  def send_push_to_users(user_profiles, incident):
      """Send push notifications instead of/in addition to email"""
      for profile in user_profiles:
          if profile.push_enabled and profile.fcm_token:
              message = messaging.Message(
                  notification=messaging.Notification(
                      title='Incident Near You',
                      body=f'Close call reported in {incident.city}'
                  ),
                  data={
                      'incident_id': str(incident.id),
                      'latitude': str(incident.latitude),
                      'longitude': str(incident.longitude),
                  },
                  token=profile.fcm_token
              )
              messaging.send(message)

  4. Mobile API Endpoints (api/views.py)

  # Register device token
  POST /api/v1/device/register
  {
      "fcm_token": "...",
      "platform": "android|ios"
  }

  # Get nearby incidents
  GET /api/v1/incidents/nearby?lat=40.0&lon=-105.0&radius=60

  # Submit incident from mobile
  POST /api/v1/incidents/create

  5. Token-based Authentication

  # Use Django REST Framework tokens or JWT
  REST_FRAMEWORK = {
      'DEFAULT_AUTHENTICATION_CLASSES': [
          'rest_framework.authentication.TokenAuthentication',
      ]
  }

  6. Modify Notification Logic

  # In utils/send_incident_emails.py, add:
  def notify_users_of_incident(incident_id, radius=60):
      """Send notifications via email AND push"""
      matched_users, incident = get_users_close_to_incident(incident_id, radius)

      # Email notifications (existing)
      send_emails(incident_id, matched_users)

      # Push notifications (new)
      send_push_to_users(matched_users, incident)

  📱 Flutter App Requirements

  1. Firebase SDK - For receiving push notifications
  2. Location permissions - To get user's current location
  3. Background location (optional) - For more accurate notifications
  4. Map integration - Google Maps or Mapbox
  5. Photo upload - For incident reports with images

  🎯 Migration Strategy

  Phase 1: API First
  - Build mobile API endpoints
  - Test with Postman/curl
  - Add device token storage

  Phase 2: Push Infrastructure
  - Set up Firebase project
  - Add FCM to Django
  - Test push notifications

  Phase 3: Flutter App
  - Build basic Flutter app
  - Register devices
  - Receive notifications
  - View incidents on map

  Phase 4: Full Featured
  - Submit incidents from mobile
  - Real-time updates
  - Photo uploads
  - User profiles

  💡 Advantages You Have

  1. Backend is solid - All the hard logic is done
  2. Data model is complete - No schema changes needed
  3. Notification logic exists - Just add new channel
  4. Location data validated - Already geocoded and tested

  🚧 Considerations

  1. User preference: Add notification_method field - "email_only", "push_only", "both"
  2. Token refresh: FCM tokens expire, need refresh logic
  3. Platform differences: iOS requires APNS, Android uses FCM
  4. Background processing: Push notifications should be fast (queue with Celery?)
  5. Rate limiting: Prevent notification spam

  Bottom line: You're 70% there. The hard parts (location matching, distance calculation, user management) are done.
   You just need to add the push notification delivery mechanism and mobile API layer.

  Would you like me to create a detailed implementation plan or start building out the mobile API endpoints now?
