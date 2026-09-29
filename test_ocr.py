from image_detector import extract_text_from_image

image_path = "test1.png"

text = extract_text_from_image(image_path)

print("\n===== OCR RESULT =====\n")
print(text)