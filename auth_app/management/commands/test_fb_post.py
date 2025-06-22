from django.core.management.base import BaseCommand
import json
from auth_app.views import _post_to_facebook

class Command(BaseCommand):
    help = 'Sends a test post to the configured Facebook Page.'

    def handle(self, *args, **options):
        self.stdout.write("Attempting to send a test post to Facebook...")
        
        message = "This is a direct test post from a command-line tool."
        result = _post_to_facebook(message)
        
        self.stdout.write("="*30)
        self.stdout.write("API Call Result:")
        self.stdout.write(json.dumps(result, indent=2))
        self.stdout.write("="*30)

        if result.get('success'):
            self.stdout.write(self.style.SUCCESS('Successfully sent the test post! Check your Facebook Page.'))
        else:
            self.stdout.write(self.style.ERROR('Failed to send the test post.')) 