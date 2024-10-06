import secrets


def generate_jwt_secret_key(length=32):
    """
    生成一個安全的 JWT 密鑰。

    :param length: 密鑰的長度，默認為 32 字節。
    :return: 生成的 JWT 密鑰。
    """
    return secrets.token_hex(length)


if __name__ == "__main__":
    secret_key = generate_jwt_secret_key()
    print(f"Key: {secret_key}")
