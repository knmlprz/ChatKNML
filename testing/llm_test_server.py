from langchain import OpenAI , PromptTemplate
from langchain.chains import LLMChain



llm = OpenAI(temperature=0, 
    max_tokens=400,
    openai_api_key="XD",
    openai_api_base="http://localhost:8000/v1"
    )

    tamplate = """Jako bot stworzony przez studentów z koła naukowego KNML, Twoim zadaniem jest odpowiadanie na pytania w 
języku polskim, aby wspierać
 polskich studentów. Proszę, przyjmij następujące polecenie lub pytanie i udziel na nie odpowiedzi w języku polskim."""
prompt = PromptTemplate(template=tamplate ,input_variables=["Q: {question}", "A: {answer}"], output="Q: {question}\nA: {answer}\n\n")

chain = LLMChain(llm=llm, prompt=few_shot_prompt)


# Ładowanie wstępnie wytrenowanego modelu Word2Vec
model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)




def preprocess_text(text):
    # Prosta funkcja do przetwarzania tekstu
    return text.lower().split()

def text_to_vector(text, model):
    # Przekształca tekst w średni wektor
    words = preprocess_text(text)
    word_vectors = [model[word] for word in words if word in model]
    if len(word_vectors) == 0:
        return np.zeros(model.vector_size)
    return np.mean(word_vectors, axis=0)

def compare_texts(text1, text2, model):
    # Oblicza podobieństwo kosinusowe między dwoma tekstami
    vector1 = text_to_vector(text1, model)
    vector2 = text_to_vector(text2, model)
   
    return cosine_similarity([vector1], [vector2])[0][0]


def log_interaction(question, true_answer , LLM_answer, similarity, LLM_language , model_name, id, log_dir="logs",step = 0 ):
    # Tworzenie unikalnego identyfikatora czasu dla każdej sesji
    current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_path = f"{log_dir}/{model_name}_{current_time}"

    # Inicjalizacja zapisywacza TensorBoard
    writer = tf.summary.create_file_writer(log_path)

    with writer.as_default():
        tf.summary.text("Question", question, step=step)
        tf.summary.text("true_answer", true_answer, step=step)
        tf.summary.text("LLM_answer", LLM_answer, step=step)
        tf.summary.text("LLM_language", LLM_language, step=step)
        tf.summary.scalar("similarity", similarity, step=step)
        tf.summary.scalar("id", id, step=step)
        
        writer.flush()

        print(len(dataset['train']))
j=0
for i in dataset['train']:
    text1=(chain(i['question'])) 
    text2=(i['answer'])
    similarity= compare_texts(text1, text2, model)
    valus[i['_id']]=  similarity
    language = detect(text1)

    log_interaction(question=i['question'], 
                    true_answer=i['answer'],
                    LLM_answer=text1,
                    similarity=similarity,
                    LLM_language=language ,
                    model_name="duzy",
                    id=i['_id'], 
                    step=j)

    j=  j+1
    if j == 2:
        break
