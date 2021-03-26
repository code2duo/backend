import unicodedata

from django.contrib.auth import get_user_model


def generate_username(email: str):
    """
    Generates username from email
    """

    User = get_user_model()

    email = email.split("@")[0]
    name = unicodedata.normalize("NFKD", email.lower()).encode("ASCII", "ignore")
    name = name.split(" ")
    lastname = name[-1]
    firstname = name[0]

    username = "%s%s" % (firstname[0], lastname)
    if User.objects.filter(username=username).count() > 0:
        username = "%s%s" % (firstname, lastname[0])
        if User.objects.filter(username=username).count() > 0:
            users = (
                User.objects.filter(username__regex=r"^%s[1-9]{1,}$" % firstname)
                .order_by("username")
                .values("username")
            )
            if len(users) > 0:
                last_number_used = list(
                    map(lambda x: int(x["username"].replace(firstname, "")), users)
                )
                last_number_used.sort()
                last_number_used = last_number_used[-1]
                number = last_number_used + 1
                username = "%s%s" % (firstname, number)
            else:
                username = "%s%s" % (firstname, 1)

    return username
