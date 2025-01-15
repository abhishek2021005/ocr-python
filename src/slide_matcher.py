from rapidfuzz import fuzz, process
import json

with open("course_data/processed_ai-1_slides.json", "r", encoding="utf-8") as file:
    slides = json.load(file)

# Sample OCR text to match
ocr_text = "Prerequisites for Al-1\n\n> Content Prerequisites: The mandatory courses in CS@FAU; Sem. 1-4, in\nparticular:\n\n> Course \u201cAlgorithmen und Datenstrukturen\u201d. (Algorithms & Data Structures)\n> Course \u201cGrundlagen der Logik in der Informatik\u201d (GLOIN). (Logic in CS)\n> Course \u201cBerechenbarkeit und Formale Sprachen\u201d. (Theoretical CS)\n> Skillset Prerequisite: Coping with mathematical formulation of the structures\n> Mathematics is the language of science (in particular computer science)\n> It allows us to be very precise about what we mean. (good for you)\n> Intuition: (take them with a kilo of salt)\n\n> This is what | assume you know! (I have to assume something)\n> In most cases, the dependency on these is partial and \u201cin spirit\u201d.\nP If you have not taken these (or do not remember), read up on them as needed!\n\n> Real Prerequisites: Motivation, interest, curiosity, hard work. (AI-1 is\nnon-trivial)\n\nP You can do this course if you want! (and | hope you are successful)\n\n= -\nEAU Rare eet aICot leer enresierellimecliinance a arbres\n"


best_match = None
highest_score = 0


for slide in slides:
    score = fuzz.partial_ratio(ocr_text, slide["slideContent"])
    if score > highest_score:
        highest_score = score
        best_match = slide


threshold = 50
if best_match and highest_score >= threshold:
    print(f"Match found with score {highest_score}:")
    print(f"Slide Content: {best_match['slideContent'][:200]}...")
    print(f"Section ID: {best_match['sectionId']}")
    print(f"Archive: {best_match['archive']}")
    print(f"Filepath: {best_match['filepath']}")
else:
    print("No good match found.")
