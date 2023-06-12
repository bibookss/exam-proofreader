from pdf2image import convert_from_path
import pytesseract 
import cv2
import os
import argparse

def convert_pdf_to_image(file_name, pdf_path):
    try:
        images = convert_from_path(pdf_path)
        folder_name = 'images'
        base_name = file_name

        image_list = []
        
        for i in range(len(images)):
            image_name = f'./{folder_name}/{base_name}-page{i}.jpg'
            image_list.append(image_name)
            images[i].save(image_name, 'JPEG')

        print("Successfully converted to images!")
    except:
        print("An error occured!")
    
    return image_list

def extract_text_from_image(image_path):
    # Load image
    img = cv2.imread(image_path)
    
    # Transform to text
    text = pytesseract.image_to_string(img)

    return text

def save_text_to_file(file_name, text):
    try:
        file = open(f'./text/{file_name}.txt', 'w')
        file.write(text)
        
        print('Successfully written to file!') 
    except:
        print('An error occured!')

def initialize_argparse():
    parser = argparse.ArgumentParser(description='A proofreading tool for exam questionnaires using ChatGPT API')
    
    parser.add_argument('file', help='the file')
    parser.add_argument('-e', '--extract', choices=['pdf', 'image'], help='extract text from a PDF file or a JPG file')
    parser.add_argument('-p', '--proofread', choices=['pdf', 'image', 'text'], help='proofread PDF, JPG, or txt file')    
    
    args = parser.parse_args()

    return args

def main():
    args = initialize_argparse()
    
    file_path = args.file
    file_name = os.path.basename(args.file).split('.')[0]
    
    if args.extract == 'pdf':
        # Convert to image 
        images = convert_pdf_to_image(file_name, file_path)
        
        # Convert to text
        text = ''
        for image in images:
            text += extract_text_from_image(image)
        
        # Save to file 
        save_text_to_file(file_name, text)

    if args.extract == 'image':
        # Convert to text
        text = extract_text_from_image(file_path)

        # Save to file
        save_text_to_file(file_name, text)


    if args.proofread == 'pdf':
        # Convert to image
        images = convert_pdf_to_image(file_name, file_path)
        
        # Convert to text
        text = ''
        for image in images:
            text += extract_text_from_image(image)

        # Proofread text

    if args.proofread == 'image':
        # Convert to text
        text = extract_text_from_image(file_path)

        # Proofread text

    if args.proofread == 'text':
        # Proofread text
        pass

    

if __name__ == '__main__':
    main()
