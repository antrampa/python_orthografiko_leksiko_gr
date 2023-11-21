from PIL import Image
import pytesseract
import os
os.environ['TESSDATA_PREFIX'] = '/usr/share/'


# Set the path to the Tesseract executable (change this based on your system)
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

def extract_greek_words(image_path, output_path):
    # Open the image file
    img = Image.open(image_path)

    # Specify the path to the tessdata folder (change '.' to your desired folder)
    tessdata_path = '.'

    # Use Tesseract to do OCR on the image
    text = pytesseract.image_to_string(img, lang='ell', config=f'--tessdata-dir {tessdata_path}')  # 'ell' is the language code for Greek
    with open("txt/text.txt", 'w', encoding='utf-8') as file1:
        file1.write(text)

    # Extract Greek words from the OCR result
    greek_words = [word for word in text.split() if any(char.isalpha() and ord(char) >= 880 and ord(char) <= 1023 for char in word)]

    # Save the Greek words to a text file
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(greek_words))

if __name__ == "__main__":
    input_image_path = "images/image.png"  # Change the extension to .png
    output_text_path = "txt/output.txt"

    extract_greek_words(input_image_path, output_text_path)
