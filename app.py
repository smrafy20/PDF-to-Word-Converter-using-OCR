from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import os
import tempfile
import shutil
from werkzeug.utils import secure_filename
import gemini  # Import your existing module

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for flashing messages
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if API key is provided
        api_key = request.form.get('api_key')
        if not api_key:
            flash('Please provide an API key')
            return redirect(request.url)
        
        # Check if file is included in the request
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        # Check for output format (default to docx if not specified)
        output_format = request.form.get('output_format', 'docx')
        if output_format not in ['docx', 'txt']:
            output_format = 'docx'  # Default to docx if invalid format specified
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process the PDF using the existing gemini module
            try:
                # Initialize the model with the provided API key
                model = gemini.setup_gemini(api_key)
                if not model:
                    flash('Failed to initialize the Gemini model. Please check your API key.')
                    return redirect(request.url)
                
                # Convert PDF to images
                image_paths, temp_dir = gemini.convert_pdf_to_images(filepath)
                if not image_paths or temp_dir is None:
                    flash('Failed to convert PDF to images.')
                    return redirect(request.url)
                
                # Extract text from images
                all_extracted_text = []
                has_errors = False
                
                for i, image_path in enumerate(image_paths):
                    if not image_path or not os.path.exists(image_path):
                        all_extracted_text.append(f"--- ERROR: Image file missing for page {i+1} ---")
                        has_errors = True
                        continue
                    
                    extracted_text = gemini.extract_text_from_image(image_path, model)
                    
                    if extracted_text is None or "--- ERROR:" in extracted_text:
                        all_extracted_text.append(extracted_text or f"--- ERROR EXTRACTING PAGE {i+1} ---")
                        has_errors = True
                    else:
                        all_extracted_text.append(extracted_text)
                
                # Save output based on selected format
                base_output_filename = os.path.splitext(filename)[0]
                
                if output_format == 'docx':
                    # Create output docx
                    output_filename = f"{base_output_filename}_extracted.docx"
                    output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
                    
                    from docx import Document
                    document = Document()
                    for page_text in all_extracted_text:
                        document.add_paragraph(page_text)
                        document.add_page_break()
                    document.save(output_path)
                else:  # txt format
                    output_filename = f"{base_output_filename}_extracted.txt"
                    output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
                    
                    with open(output_path, 'w', encoding='utf-8') as txt_file:
                        for i, page_text in enumerate(all_extracted_text):
                            txt_file.write(page_text)
                            if i < len(all_extracted_text) - 1:
                                txt_file.write("\n\n--- Page Break ---\n\n")
                
                # Clean up temporary directory
                if temp_dir and os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
                
                # If there were errors during processing
                if has_errors:
                    flash('Some pages could not be processed correctly. Please check the downloaded file.')
                
                # Provide download page
                return render_template('download.html', filename=output_filename, format=output_format)
            
            except Exception as e:
                flash(f'An error occurred during processing: {str(e)}')
                return redirect(request.url)
            finally:
                # Clean up the uploaded file
                if os.path.exists(filepath):
                    os.remove(filepath)
        else:
            flash('File type not allowed. Please upload a PDF file.')
            return redirect(request.url)
    
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(file_path):
        flash('The requested file does not exist.')
        return redirect(url_for('index'))
    
    return send_file(file_path, as_attachment=True)

@app.errorhandler(413)
def too_large(e):
    flash('File is too large (maximum size is 16MB).')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)