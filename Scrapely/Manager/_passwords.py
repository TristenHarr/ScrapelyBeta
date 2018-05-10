from passlib.hash import pbkdf2_sha256


def make_password(password):
    # TODO: Rewrite this, increase security, look into some kind of database-row rotations
    hashed = pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)
    return hashed


def check_password(password, hashed):
    return pbkdf2_sha256.verify(password, hashed)
