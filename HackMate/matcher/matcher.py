# matcher/matcher.py

import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Carga el modelo de spaCy (modelo pequeño, en inglés)
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    """
    Procesa el texto utilizando spaCy:
      - Pasa a minúsculas
      - Lematiza las palabras
      - Elimina tokens de puntuación y stopwords
    """
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)

def vectorize_texts(texts):
    """
    Recibe una lista de textos y devuelve la matriz TF-IDF.
    """
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(texts)
    return vectors

def compute_similarity(vector1, vector2):
    """
    Calcula la similitud coseno entre dos vectores.
    """
    return cosine_similarity(vector1, vector2)[0][0]

def is_complementary(desc1, desc2):
    """
    Regla heurística simple para determinar complementariedad.
    Por ejemplo, si un perfil menciona 'ux' o 'ui' y el otro 'fullstack', consideramos que son complementarios.
    Puedes agregar más reglas según sea necesario.
    """
    # Convierte a minúsculas para facilitar la comparación
    d1 = desc1.lower()
    d2 = desc2.lower()
    # Ejemplo básico:
    if (("ux" in d1 or "ui" in d1) and "fullstack" in d2) or (("ux" in d2 or "ui" in d2) and "fullstack" in d1):
        return True
    return False

def matching_algorithm(user_profiles):
    """
    user_profiles: lista de diccionarios, cada uno con al menos:
        'user_id' y 'business_description'
    Realiza un matching sencillo basado en TF-IDF y reglas de complementariedad.
    
    Devuelve una lista de tuplas: (user_id_1, user_id_2, score)
    """
    processed_desc = []
    user_ids = []
    
    # Preprocesa las descripciones
    for user in user_profiles:
        desc = user.get("business_description", "")
        processed = preprocess_text(desc)
        processed_desc.append(processed)
        user_ids.append(user["user_id"])
    
    # Genera la matriz TF-IDF
    vectors = vectorize_texts(processed_desc)
    
    matches = []
    used_users = set()
    
    n_users = len(user_ids)
    for i in range(n_users):
        # Evita emparejar de nuevo usuarios ya asignados en esta búsqueda
        if user_ids[i] in used_users:
            continue
        best_match = None
        best_score = 0.0
        for j in range(i + 1, n_users):
            if user_ids[j] in used_users:
                continue
            # Calcula similitud coseno
            sim = compute_similarity(vectors[i], vectors[j])
            # Si las descripciones son complementarias, aumenta el score (ejemplo boost de 0.2)
            if is_complementary(processed_desc[i], processed_desc[j]):
                sim += 0.2
            if sim > best_score and sim >= 0.5:  # Umbral arbitrario, ajustar según pruebas
                best_score = sim
                best_match = user_ids[j]
        if best_match is not None:
            matches.append((user_ids[i], best_match, best_score))
            used_users.add(user_ids[i])
            used_users.add(best_match)
    return matches

if __name__ == "__main__":
    # Ejemplo de uso con datos simulados
    sample_users = [
        {"user_id": 1, "business_description": "I am a UX/UI designer focused on creating intuitive interfaces."},
        {"user_id": 2, "business_description": "I work as a fullstack developer building scalable web applications."},
        {"user_id": 3, "business_description": "I specialize in marketing and digital growth strategies."},
        {"user_id": 4, "business_description": "I am a UX/UI expert with a passion for user-centered design."},
    ]
    matches = matching_algorithm(sample_users)
    print("Matches encontrados:")
    for match in matches:
        print(f"Usuario {match[0]} emparejado con Usuario {match[1]} con score {match[2]:.2f}")
