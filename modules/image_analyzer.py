from PIL import Image

def analyze_image(image_path):
    """
    Analizuje obraz i zwraca informacje o jego rozmiarze i trybie koloru.

    Args:
        image_path (str): Ścieżka do pliku obrazu.

    Returns:
        dict: Słownik zawierający informacje o obrazie lub komunikat o błędzie.
    """
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            mode = img.mode
            return {
                "width": width,
                "height": height,
                "mode": mode
            }
    except FileNotFoundError:
        return {"error": "Image not found"}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}

# Przykładowe użycie (wymaga pliku image.jpg)
if __name__ == "__main__":
    image_analysis = analyze_image("image.jpg") # Zamień na istniejący plik obrazu
    print(image_analysis)