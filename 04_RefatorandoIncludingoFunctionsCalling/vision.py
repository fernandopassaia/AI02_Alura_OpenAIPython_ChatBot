import os

from dotenv import load_dotenv
from openai import OpenAI

from helpers import encode_image

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-4o"


def analyse_image(image):
    # note que no meu prompt eu aviso a OpenAI API que eu estou enviando uma imagem
    prompt = """"
        Assuma que você é um assistente de chatbot e que provavelmente o usuário está enviado a foto de
        um produto. Faça uma análise dele, e se for um produto com defeito, emita um parecer. Assuma que você sabe e
        processou uma imagem com o Vision e a resposta será informada no formato de saída.

        # FORMATO DA RESPOSTA
       
         Minha análise para imagem consiste em: Parecer com indicações do defeito ou descrição do produto (se não 
         houver defeito)

        ## Descreva a imagem
        coloque a descrição aqui
    """

    # vision geralmente trabalha com uma URL, como estou em localhost, vou encodar 64 e enviar pra ele...
    image_base64 = encode_image(image)

    response = client.chat.completions.create(
        model=model,  # note que o modelo aqui é o Vision, apenas ele pode processar imagens
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}",
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )

    return response.choices[0].message.content


print(analyse_image("data/canecaCafe.png"))
print(analyse_image("data/canecaQuebrada.png"))
print(analyse_image("data/fernando.png"))
