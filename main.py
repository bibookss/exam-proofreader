from pdf2image import convert_from_path
import pytesseract 
import cv2
import os
import argparse
import openai

def initialize_folders():
    if not os.path.exists('images'):
        os.mkdir('images')
        print('images directory created!')
    if not os.path.exists('text'):
        os.mkdir('text')
        print('text directory created!')

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

        print('Successfully converted to images!')
    except:
        print('An error occured!')
    
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

def proofread_text(text):
    openai.api_key = os.getenv("API_KEY")
    
    prompt = 'You are a professional proofreader working for an elementary school. Your job is to correct the grammar and strucure of the exam. The response should be in markdown. Highlight the changes you made by making adding a strikethrough to the words or phrase you will not need while also adding in bold the changes you made. The exam is as follow: ' 


    _model = 'gpt-3.5-turbo'
    _message = [{ 'role': 'user', 'content' : prompt + text }]
    
    print (_message)

    response = openai.ChatCompletion.create(
        model = _model,
        message = _message
    )

    return response.choices[0].message['content']


def main():
    initialize_folders()
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
        new_text = proofread_text(text)

        # Save text
        p_file_name = f'PR-{file-name}'
        save_text_to_file(p_file_name, text)

    if args.proofread == 'image':
        # Convert to text
        text = extract_text_from_image(file_path)

        # Proofread text
        new_text = proofread_text(text)
        
        # Save text
        p_file_name = f'PR-{file_name}'
        save_text_to_file(p_file_name, text)

    if args.proofread == 'text':
        text = file_path

        # Proofread text
        new_text = proofread_text(text)

        # Save text
        p_file_name = f'PR-{file_name}'
        save_text_to_file(p_file_name, text)
    

if __name__ == '__main__':
    main()
