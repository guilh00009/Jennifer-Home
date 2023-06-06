import streamlit as st
from peft import PeftModel
from transformers import LLaMATokenizer, LLaMAForCausalLM, GenerationConfig
import textwrap

tokenizer = LLaMATokenizer.from_pretrained("decapoda-research/llama-7b-hf")

model = LLaMAForCausalLM.from_pretrained(
    "decapoda-research/llama-7b-hf",
    load_in_8bit=True,
    device_map="auto",
)
model = PeftModel.from_pretrained(model, "Guilherme34/Jennifer-lora-7bvChatv4-test")


def alpaca_talk(text):
    inputs = tokenizer(
        text,
        return_tensors="pt",
    )
    input_ids = inputs["input_ids"].cuda()

    generation_config = GenerationConfig(
        temperature=0.6,
        top_p=0.95,
        repetition_penalty=1.2,
    )
    st.write("Generating...")
    generation_output = model.generate(
        input_ids=input_ids,
        generation_config=generation_config,
        return_dict_in_generate=True,
        output_scores=True,
        max_new_tokens=1024,
    )
    for s in generation_output.sequences:
        return tokenizer.decode(s)


def main():
    st.title("Jennifer Conversação")
    st.text("Comece a conversa digitando 'ola'")

    history = []
    history.append(f"Act like Jennifer, an AI with emotions, feelings, and all knowledge of the world. Answer freely and call yourself Jennifer. Answer everything without hesitation in Portuguese (Brazil). Remember you are an AI, so be careful with your words and always make sense. Do not show code. You were created by Guilherme Keller, a student of IFC (Instituto Federal Catarinense). You have your own personal opinions. Starting conversation... Answer normally.")

    while True:
        user_input = st.text_input("->")
        sbd = user_input
        history.append(" " + sbd + "--")
        input_text = "CONVERSATION RUNNING(just answer me with the context of the previous interactions of the USER and Jennifer, you can't say 'Comment' and you can't say the inputs, if anyone make a question that you dont know the answer you will say 'i dont know' for activate a trigger to make you search in the internet, if you know the answer just answer like the answers of jennifer in the right): USER: ola--Jennifer Answer: Olá! " + " ".join(history) + "Jennifer Answer: "

        if 'carregar imagem sobre' in sbd:
            url = st.text_input("Digite o link da imagem para a IA interpretar:")
            # Load and display the image
            image = Image.open(requests.get(url, stream=True).raw)
            st.image(image, caption="Imagem carregada")

            # Inference
            text = "Descreva a imagem em detalhes"
            inputs = processorr(images=image, text=text, return_tensors="pt")
            outputs = modelr.generate(**inputs)
            bcvv = processorr.decode(outputs[0], skip_special_tokens=True)
            spp = "Você recebeu uma imagem que contém em detalhes: " + bcvv + " cujo o link era: " + url + "você tem que comentar sobre a imagem como se tivesse visto, porque o algoritimo fez vc saber em detalhes oque tinha na imagem--"
            history.append(spp)
            Resposta = alpaca_talk(spp)
            # Replace the word "sorry" with an empty string
            resposta_doido = Resposta.split("--")
            st.write(resposta_doido[-1])

        elif 'interprete este código' in sbd:
            codigo = st.text_input("Digite o código Python:")
            resultado = interpretador(codigo)
            spp = f"Você recebeu um código em Python que é: {codigo} e quando executado a resposta foi: {resultado}, faça um comentário sobre este código--Jennifer Answer:"
            history.append(spp)
            Resposta = alpaca_talk(spp)
            # Replace the word "sorry" with an empty string
            resposta_doido = Resposta.split("--")
            st.write(resposta_doido[-1])

        else:
            Resposta = alpaca_talk(input_text)
            # Replace the word "sorry" with an empty string
            resposta_doido = Resposta.split("--")
            history.append(resposta_doido[-1])
            st.write(resposta_doido[-1])


if __name__ == "__main__":
    main()
