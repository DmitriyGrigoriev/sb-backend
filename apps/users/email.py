from djoser import email
# from .token import rest_authtoken_generator


class ActivationEmail(email.ActivationEmail):
    template_name = 'email/activation.html'

    # def get_context_data(self):
    #     # ActivationEmail can be deleted
    #     context = super().get_context_data()
    #
    #     user = context.get("user")
    #     context["token"] = rest_authtoken_generator.make_token(user)
    #     return context

class ConfirmationEmail(email.ConfirmationEmail):
    template_name = "email/confirmation.html"

class PasswordResetEmail(email.PasswordResetEmail):
    template_name = "email/password_reset.html"

    # def get_context_data(self):
    #     context = super().get_context_data()
    #
    #     user = context.get("user")
    #     context["token"] = rest_authtoken_generator.make_token(user)
    #     return context

class PasswordChangedConfirmationEmail(email.PasswordChangedConfirmationEmail):
    template_name = "email/password_changed_confirmation.html"

class UsernameChangedConfirmationEmail(email.UsernameChangedConfirmationEmail):
    template_name = "email/username_changed_confirmation.html"

class UsernameResetEmail(email.UsernameResetEmail):
    template_name = "email/username_reset.html"

    # def get_context_data(self):
    #     context = super().get_context_data()
    #
    #     user = context.get("user")
    #     context["token"] = rest_authtoken_generator.make_token(user)
    #     return context