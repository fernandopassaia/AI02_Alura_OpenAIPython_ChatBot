import base64


def load(filename):
    try:
        with open(filename, "r") as file:
            data = file.read()
            return data
    except IOError as e:
        print(f"Erro ao carregar o arquivo: {e}")


def save(filename, data):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(data)
    except IOError as e:
        print(f"Erro ao salvar o arquivo: {e}")


def encode_image(filename):
    with open(filename, "rb") as file:  # leio o arquivo e retorno encodado em base64
        return base64.b64encode(file.read()).decode("utf-8")
