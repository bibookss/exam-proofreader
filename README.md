## Exam Proofreader
An exam proofreading program using AI to automatically generate the correct grammar and structure of an exam question and answer.

### Installation
Install the dependencies
```
pip install -r requirements.txt
```

Install Tesseract
```
sudo apt install tesseract-ocr -y
```

### Usage
```
python3 main.py [-h] [-e {pdf,image}] [-p {pdf,image,text}] file
```
```
positional arguments:
  file                  the file

options:
  -h, --help            show this help message and exit
  -e {pdf,image}, --extract {pdf,image}
                        extract text from a PDF file or a JPG file
  -p {pdf,image,text}, --proofread {pdf,image,text}
                        proofread PDF, JPG, or txt file
```
