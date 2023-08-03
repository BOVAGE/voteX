import string
import secrets
from django.utils.crypto import get_random_string

alphabet = string.ascii_letters + string.digits


def generate_password(length=8):
    while True:
        password = "".join(secrets.choice(alphabet) for i in range(length))
        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and sum(c.isdigit() for c in password) >= 3
        ):
            break
    return password


def generate_unique_pass_name(instance, new_pass_name=None):
    if new_pass_name is not None:
        pass_name = new_pass_name
    else:
        pass_name = get_random_string(8)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(pass_name=pass_name).exists()
    if qs_exists:
        new_pass_name = f"{pass_name}{secrets.token_hex(2)}"
        return generate_unique_pass_name(instance, new_pass_name=new_pass_name)
    return pass_name
