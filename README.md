# Telugu OCR (Text Recognition) Project

## Project Objective
The primary goal of this project is to digitize Telugu text from user-provided PDFs. By allowing users to upload PDFs, extract the Telugu text, and download it in JSON format, this project aims to facilitate the collection and digitization of Telugu textual data. This process enhances the accessibility and usability of Telugu texts for various applications, including research, archiving, and data analysis.

## Key Features
1. **User Interface:** The project employs a user-friendly interface built with Gradio, enabling users to easily upload their PDFs and manage the text extraction process.
2. **Image Processing Techniques:** The project leverages multiple image processing methods to optimize text extraction:
    - Rescaling images
    - Gamma correction
    - Adaptive thresholding
    - Edge detection
    - Morphological transformations
3. **Optical Character Recognition (OCR):** Pytesseract is utilized to perform OCR on processed images, ensuring accurate extraction of Telugu text.
4. **PDF Handling:** The pdf2image library is used to convert PDF pages to images for further processing.
5. **JSON Output:** The extracted text is saved in a structured JSON format, making it easy to download and use for further analysis or storage.

## Detailed Code Overview

### Import the necessary libraries:

1. **OpenCV (cv2):** A powerful library for computer vision and image processing tasks. It is used here to manipulate images, such as reading, writing, and performing various transformations.
2. **NumPy (np):** A fundamental package for numerical computations in Python. It provides support for arrays, matrices, and a plethora of mathematical functions to operate on these data structures.
3. **PyTesseract:** A Python wrapper for Google's Tesseract-OCR Engine, allowing us to perform optical character recognition (OCR) on images to extract text.
4. **pdf2image:** A library used to convert PDF files into images. The convert_from_path function converts each page of a PDF into an image, enabling us to process the contents of PDFs.
5. **Gradio:** A library for building user-friendly web interfaces for machine learning models and data processing scripts. It helps in creating interactive UIs that can run in a web browser.
6. **JSON:** A module to handle JSON (JavaScript Object Notation) data. It allows parsing JSON formatted data and converting Python objects to JSON.
7. **OS:** This module provides a way of interacting with the operating system. It is used for tasks such as file and directory manipulation.

### Function Explanations

1. **rescaleFrame for Image Resizing:** 
   - This function resizes an image or frame by a specified scaling factor (default: 0.75). It computes the new dimensions based on the original size and the scaling factor and uses the OpenCV library to resize the image.
   
2. **apply_gamma for Gamma Correction:** 
   - This function applies gamma correction to an image, enhancing its brightness. It uses a lookup table based on the inverse gamma value to adjust pixel values, improving image quality.

3. **adaptive_threshold for Adaptive Thresholding:** 
   - This function converts a grayscale image into a binary image using adaptive thresholding, which is effective for images with varying lighting conditions.

4. **edge_detection for Edge Detection:** 
   - This function performs edge detection on an image using the Canny algorithm, highlighting areas of rapid intensity change.

5. **morphological_transformation for Morphological Transformations:** 
   - This function applies morphological transformations to an image, such as closing small holes and gaps, to prepare it for text extraction.

6. **process_image for Image Processing:** 
   - This function processes an image using different methods (default, adaptive_threshold, edge_detection, morphological) to prepare it for text extraction.

7. **extract_text_from_image for Text Extraction:** 
   - This function uses Tesseract OCR to extract text from a processed image, specifically handling Telugu text.

### Directory and Dictionary Initialization
- Initializes an output directory and a dictionary to store the extracted text from each page. Creates the directory if it does not exist.

### PDF Handling Functions

1. **save_and_next for Saving and Processing Next Page:** 
   - Handles saving the extracted text from the current page and processing the next page, updating the interface with new content.
   
2. **skip_page for Skipping a Page:** 
   - Allows skipping the current page and moving to the next page without saving the text.
   
3. **upload_pdf for PDF Upload and Initial Processing:** 
   - Handles uploading a PDF file and converting its pages to images, initializing the interface with the first page's image and extracted text.

4. **navigate_to_page for Page Navigation:** 
   - Allows navigating to a specific page in the PDF, updating the interface with the specified page's content.

### User Interface with Gradio

1. **display_pdf_and_text for User Interface:** 
   - Creates a user interface using Gradio, including components for uploading PDFs, displaying page images, editing extracted text, navigating pages, and saving results.
   
2. **Interface Initialization:** 
   - Initializes and launches the Gradio interface, allowing users to interact with the PDF processing tool.

### Gradio Library Features
- **Ease of Use:** High-level API for quick UI component creation.
- **Interactivity:** Intuitive UI elements for user interaction.
- **Flexibility:** Supports various input types and output formats.
- **Deployment:** Simplifies model hosting and web interface access.
- **Community and Ecosystem:** Integration with popular libraries and community support.

### Deploying the Model using Hugging Face

1. **Choose a Hugging Face Model:** 
   - Select a suitable model for text extraction from Hugging Face's Model Hub.

2. **Model Integration:** 
   - Integrate the chosen model into the codebase, typically using the transformers library.

3. **Deployment with Gradio:** 
   - Encapsulate the model within a Gradio interface function.

4. **Input and Output Handling:** 
   - Ensure the interface handles inputs and outputs effectively.

5. **Testing and Iteration:** 
   - Thoroughly test the functionality and performance of the integrated model within the Gradio interface.

## Requirements

- opencv-python==4.10.0.82
- opencv-python-headless==4.10.0.82
- numpy==1.26.4
- pytesseract==0.3.10
- pdf2image==1.17.0
- gradio==4.36.1
- gradio_client==1.0.1
- json5==0.9.25
- jsonpointer==2.4
- jsonschema==4.22.0
- jsonschema-specifications==2023.12.1
- fastjsonschema==2.19.1
- orjson==3.10.4
- ujson==5.10.0
- python-json-logger==2.0.7

These libraries collectively enable various functionalities in your Python project, ranging from computer vision tasks (OpenCV and numpy) to text extraction from images (pytesseract), PDF processing (pdf2image), model deployment (Gradio), and JSON handling and validation. Each library version specified ensures compatibility and stability within your project environment.

## Conclusion
This project significantly contributes to the digitization of Telugu texts by providing a robust and user-friendly tool for extracting text from PDFs. The use of advanced image processing and OCR techniques ensures high accuracy in text extraction, facilitating the creation of valuable digital archives of Telugu literature and documents.


