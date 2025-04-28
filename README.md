# PDF Text Extractor with Google Gemini AI

A web application that uses Google's Gemini AI to extract text from PDF documents. This tool is especially effective for multilingual documents and can handle Bangla text.

## Features

- Upload PDF files through a user-friendly web interface
- Convert PDFs to images for better processing
- Extract text from images using Google's Gemini AI model
- Save extracted text as Word (DOCX) or plain text (TXT) documents
- Format selection option for output files
- Support for multilingual text extraction

## Prerequisites

Before running this application, you'll need:

1. Python 3.8 or higher
2. A Google Gemini API key (get one from [Google AI Studio](https://ai.google.dev/))
3. The dependencies listed in the requirements.txt file

## Installation

1. Clone or download this repository to your local machine

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. For PDF to image conversion, you'll need Poppler installed:

   - **Windows users**:
     - Download Poppler for Windows from [here](https://github.com/oschwartz10612/poppler-windows/releases/)
     - Extract the downloaded file
     - Add the `bin` directory to your PATH environment variable:
       1. Right-click on "This PC" or "My Computer" and select "Properties"
       2. Click on "Advanced system settings"
       3. Click on "Environment Variables"
       4. Under "System variables", find the "Path" variable, select it and click "Edit"
       5. Click "New" and add the path to the bin folder (e.g., `C:\path\to\poppler-xx\bin`)
       6. Click "OK" to close all dialogs

   - **Mac users**:
     ```
     brew install poppler
     ```

   - **Linux users**:
     ```
     sudo apt-get install poppler-utils
     ```

## Usage

1. Start the application:
   ```
   python app.py
   ```

2. Open your web browser and go to:
   ```
   http://localhost:5000
   ```

3. Use the web interface to:
   - Enter your Google Gemini API key
   - Upload a PDF file (maximum size: 16MB)
   - Click "Extract Text" to process the file
   - Download the extracted text as a .docx or .txt file

## Configuration

The application uses the following default settings:

- Upload folder: `./uploads` (created automatically)
- Maximum file size: 16MB
- Allowed file extensions: PDF only
- DPI for image conversion: 300

## Project Structure

```
.
├── app.py                 # Flask web application
├── gemini.py              # Core PDF processing and AI text extraction logic
├── requirements.txt       # Python dependencies
├── templates/             # HTML templates
│   ├── index.html         # Main upload page
│   └── download.html      # Download page
└── uploads/               # Folder for storing uploaded files and results
```

## Troubleshooting

- **"Failed to initialize the Gemini model"**: Check that your API key is correct and has access to the Gemini model.
- **"Failed to convert PDF to images"**: Make sure Poppler is installed correctly and in your PATH.
- **Processing takes a long time**: This is normal for large or complex PDFs. The extraction process involves converting each page to an image and sending it to the Gemini API.
- **Some text is not extracted correctly**: The accuracy depends on the quality of the PDF and how the text is represented (as text or as images).

## License

[MIT License](LICENSE)

## Acknowledgements

- This project uses Google's Gemini AI model for text extraction
- PDF to image conversion is handled by the pdf2image library