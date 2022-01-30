from django.contrib.auth import tokens

from rest_framework.authtoken.models import Token

class TokenGenerator(tokens.PasswordResetTokenGenerator):
    def make_token(self, user):
        """
        Return a token that can be used once to do a password reset
        for the given user.
        """
        return Token.generate_key()

    def check_token(self, user, token):
        """
        Check that a password reset token is correct for a given user.
        """
        if not (user and token):
            return False

        try:
            value, _ = Token.objects.get_or_create(user=user)
        except ValueError:
            return False

        if not (value.key == token):
            return False

        return True


rest_authtoken_generator = TokenGenerator()