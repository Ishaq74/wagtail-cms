import os
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.admin.panels import FieldPanel, HelpPanel
from django import forms
from cryptography.fernet import Fernet
from django.core.mail import EmailMessage, get_connection
import smtplib
from django.db import models

# Clé Fernet sécurisée
FERNET_SECRET_KEY = b"nNjpIl9Ax2LRtm-p6ryCRZ8lRsL0DtuY0f9JeAe2wG0="

if not FERNET_SECRET_KEY:
    raise RuntimeError("FERNET_SECRET_KEY is not defined in the environment variables.")

@register_setting
class SMTPSettings(BaseSiteSetting):
    email_host = models.CharField(max_length=255, verbose_name="Email Host")
    email_port = models.PositiveIntegerField(verbose_name="Email Port")
    email_host_user = models.CharField(max_length=255, verbose_name="Email Host User")
    email_host_password = models.TextField(verbose_name="Email Host Password")
    use_tls = models.BooleanField(default=True, verbose_name="Use TLS")
    use_ssl = models.BooleanField(default=False, verbose_name="Use SSL")
    test_email_recipient = models.EmailField(
        verbose_name="Test Email Recipient",
        default="admin@example.com",
        help_text="Enter the email address to receive the test email.",
    )

    class Meta:
        verbose_name = "SMTP Settings"
        verbose_name_plural = "SMTP Settings"

    def encrypt_password(self, password):
        cipher = Fernet(FERNET_SECRET_KEY)
        return cipher.encrypt(password.encode()).decode()

    def decrypt_password(self):
        cipher = Fernet(FERNET_SECRET_KEY)
        return cipher.decrypt(self.email_host_password.encode()).decode()

    def validate_smtp_settings(self):
        """Validate that all required SMTP settings are configured."""
        required_settings = {
            'email_host': self.email_host,
            'email_port': self.email_port,
            'email_host_user': self.email_host_user,
            'email_host_password': self.email_host_password,
        }
        missing_settings = [key for key, value in required_settings.items() if not value]

        if missing_settings:
            missing_fields = ', '.join(missing_settings)
            return False, f"Les paramètres SMTP suivants ne sont pas configurés : {missing_fields}"
        return True, "Tous les paramètres SMTP sont configurés."

    def save(self, *args, **kwargs):
        if not self.email_host_password.startswith("gAAAA"):
            self.email_host_password = self.encrypt_password(self.email_host_password)
        super().save(*args, **kwargs)

    def test_smtp_connection(self):
        """Test the SMTP connection."""
        valid, message = self.validate_smtp_settings()
        if not valid:
            return False, message

        try:
            connection = smtplib.SMTP(host=self.email_host, port=self.email_port)
            if self.use_tls:
                connection.starttls()
            connection.login(self.email_host_user, self.decrypt_password())
            connection.quit()
            return True, "SMTP Connection successful!"
        except smtplib.SMTPAuthenticationError:
            return False, "Authentication failed. Check your username or password."
        except smtplib.SMTPConnectError:
            return False, "Unable to connect to the SMTP server. Check the host or port."
        except Exception as e:
            return False, f"An unexpected error occurred: {e}"

    def send_test_email(self):
        """Send a test email and verify delivery."""
        valid, message = self.validate_smtp_settings()
        if not valid:
            return False, message

        try:
            connection = get_connection(
                backend='django.core.mail.backends.smtp.EmailBackend',
                host=self.email_host,
                port=self.email_port,
                username=self.email_host_user,
                password=self.decrypt_password(),
                use_tls=self.use_tls,
                fail_silently=False,
            )

            email = EmailMessage(
                subject="SMTP Test Email",
                body="This is a test email sent from your SMTP configuration.",
                from_email=self.email_host_user,
                to=[self.test_email_recipient],
                connection=connection,
            )
            sent_count = email.send(fail_silently=False)

            if sent_count == 0:
                return False, "L'email n'a pas été accepté par le serveur SMTP. Vérifiez les paramètres ou l'adresse du destinataire."
            return True, "Test email sent successfully!"
        except smtplib.SMTPRecipientsRefused:
            return False, "The recipient address was rejected by the server."
        except smtplib.SMTPAuthenticationError:
            return False, "Authentication failed. Check your username or password."
        except smtplib.SMTPException as e:
            return False, f"SMTP error during email sending: {e}"
        except Exception as e:
            return False, f"An unexpected error occurred: {e}"

    panels = [
        FieldPanel("email_host"),
        FieldPanel("email_port"),
        FieldPanel("email_host_user"),
        FieldPanel("email_host_password", widget=forms.PasswordInput(render_value=True)),
        FieldPanel("use_tls"),
        FieldPanel("use_ssl"),
        FieldPanel("test_email_recipient"),
        HelpPanel(
            content=(
                '<a href="/admin/smtp/test-smtp/" class="button button--primary">'
                "Tester la connexion SMTP</a> "
                '<a href="/admin/smtp/send-test-email/" class="button">'
                "Envoyer un email de test</a>"
            )
        ),
    ]
