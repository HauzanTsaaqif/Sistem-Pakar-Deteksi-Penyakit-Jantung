import tkinter as tk
from PIL import Image, ImageTk

knowledge_base = {
    "G1,G3,G4": "P001 - Bulai (White color like flour on leaves)",  # Bulai
    "G6,G8,G9,G10": "P002 - Blight (Elongated light brown patches)",  # Blight
    "G15,G16,G17,G19": "P004 - Burn (Swelling of the cob)",  # Burn
    "G28,G29,G31": "P006 - Cob Borer (Transverse holes in leaves)",  # Cob Borer
}


def calculate_similarity(input_symptoms, rule_symptoms):
    input_set = set(input_symptoms)
    rule_set = set(rule_symptoms.split(","))

    matching_symptoms = input_set.intersection(rule_set)
    non_matching_symptoms = input_set - rule_set
    match_score = len(matching_symptoms) / len(rule_set)

    penalty_score = len(non_matching_symptoms) * 0.1
    final_score = max(match_score - penalty_score, 0)

    return final_score


def forward_chaining(input_symptoms, knowledge_base, threshold=0.3):
    best_match = None
    highest_score = 0

    for rule, disease in knowledge_base.items():
        score = calculate_similarity(input_symptoms, rule)
        if score > highest_score and score >= threshold:
            highest_score = score
            best_match = disease

    if best_match:
        return f"Penyakit yang terdeteksi: {best_match} dengan kecocokan {highest_score * 100:.2f}%"
    else:
        return "Tidak ada penyakit yang cocok dengan gejala yang diberikan."


def next_question(answer):
    global current_question_index
    if answer == "Ya":
        selected_symptoms.append(
            current_question_key
        )  # Tambahkan gejala jika jawab 'Ya'

    current_question_index += 1
    if current_question_index < len(symptom_questions):
        update_question()
    else:
        diagnose()


def update_question():
    global current_question_key
    current_question_key = list(symptom_questions.keys())[current_question_index]
    question_label.config(text=symptom_questions[current_question_key])


def diagnose():
    result = forward_chaining(selected_symptoms, knowledge_base, threshold=0.3)
    question_label.config(text="Hasil Diagnosa:")
    text_result.insert(tk.END, result)
    text_result.pack(pady=10)
    button_restart.pack(pady=10)
    button_yes.pack_forget()
    button_no.pack_forget()


def restart_diagnosis():
    global selected_symptoms, current_question_index
    selected_symptoms = []
    current_question_index = 0
    text_result.delete(1.0, tk.END)
    text_result.pack_forget()
    button_restart.pack_forget()
    update_question()
    button_yes.pack(side="left", padx=10)
    button_no.pack(side="right", padx=10)


def start_diagnosis():
    button_start.pack_forget()
    update_question()
    button_yes.pack(side="left", padx=10)
    button_no.pack(side="right", padx=10)


root = tk.Tk()
root.title("Sistem Pakar Diagnosis Penyakit Jagung")
root.geometry("600x400")

background_image = Image.open("bg_corn.jpg")
background_image = background_image.resize((600, 400))
background_photo = ImageTk.PhotoImage(background_image)

background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

symptom_questions = {
    "G1": "Apakah daun menguning atau klorosis?",
    "G3": "Apakah muncul warna putih seperti tepung\npada permukaan daun?",
    "G4": "Apakah daun melengkung atau menggulung?",
    "G6": "Apakah daun tampak layu?",
    "G8": "Apakah terdapat bercak coklat muda\nmemanjang berbentuk gulungan?",
    "G9": "Apakah muncul bercak coklat berbentuk\nelips pada daun?",
    "G10": "Apakah daun tampak kering?",
    "G15": "Apakah tongkol jagung terlihat membengkak?",
    "G16": "Apakah ada jamur putih hingga hitam\npada biji jagung?",
    "G17": "Apakah biji jagung membengkak?",
    "G19": "Apakah kelobot terbuka dan\nmenunjukkan jamur?",
    "G28": "Apakah terdapat lubang melintang\npada daun?",
    "G29": "Apakah rambut tongkol terpotong\natau mengering?",
    "G31": "Apakah sering terlihat larva\ndi tanaman jagung?",
}

selected_symptoms = []
current_question_index = 0
current_question_key = ""

frame = tk.Frame(root, bg="white")
frame.pack(pady=20)

question_label = tk.Label(
    frame, text="Corn Diseases Detection", font=("Helvetica", 14), bg="white"
)
question_label.pack(pady=0)

button_start = tk.Button(
    frame, text="Mulai Diagnosa", command=start_diagnosis, width=20, height=2
)
button_start.pack(pady=0)

button_restart = tk.Button(
    root, text="Deteksi Kembali", command=restart_diagnosis, width=20, height=2
)

text_result = tk.Text(root, height=5, width=50)

button_yes = tk.Button(
    root, text="Ya", command=lambda: next_question("Ya"), width=10, height=2
)
button_no = tk.Button(
    root, text="Tidak", command=lambda: next_question("Tidak"), width=10, height=2
)

button_frame = tk.Frame(root)
button_frame.pack(side="bottom", pady=0)

root.mainloop()
