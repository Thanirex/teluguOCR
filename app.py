# %%
import cv2 as cv
import numpy as np
import pytesseract
from pdf2image import convert_from_path
import gradio as gr
import json
import os

# Function to rescale the frame
def rescaleFrame(frame, scale=0.75):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

# Function to apply gamma correction
def apply_gamma(image, gamma=1.0):
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    return cv.LUT(image, table)

# Function to apply adaptive thresholding
def adaptive_threshold(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    return cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)

# Function to apply edge detection
def edge_detection(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    return cv.Canny(gray, 50, 150)

# Function to apply morphological transformations
def morphological_transformation(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    _, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    return cv.morphologyEx(binary, cv.MORPH_CLOSE, kernel)

# Function to process image for text extraction
def process_image(img, method='default'):
    resized_image = rescaleFrame(img)

    if method == 'default':
        gray = cv.cvtColor(resized_image, cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(gray, (3, 3), 0)
        gamma_corrected = apply_gamma(blur, gamma=0.3)
        _, thresh = cv.threshold(gamma_corrected, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
        return cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel)
    elif method == 'adaptive_threshold':
        return adaptive_threshold(resized_image)
    elif method == 'edge_detection':
        return edge_detection(resized_image)
    elif method == 'morphological':
        return morphological_transformation(resized_image)

# Function to extract text from processed image
def extract_text_from_image(image, langs='tel'):
    return pytesseract.image_to_string(image, lang=langs)

output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

all_texts = {}

def save_and_next(page_num, text, extracted_texts, original_images, total_pages):
    page_num = int(page_num)  # Ensure page_num is an integer
    formatted_text = {
        f"Page number: {page_num}": {
            "Content": [
                line for line in text.split('\n') if line.strip() != ''
            ]
        }
    }
    all_texts.update(formatted_text)
    json_path = os.path.join(output_dir, "all_texts.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(all_texts, f, ensure_ascii=False, indent=4)

    next_page_num = page_num + 1  # Increment to next page
    if next_page_num <= total_pages:
        next_page_image = original_images[next_page_num - 1]
        methods = ['default', 'adaptive_threshold', 'edge_detection', 'morphological']
        best_text = ""
        max_confidence = -1
        for method in methods:
            processed_image = process_image(next_page_image, method=method)
            text = extract_text_from_image(processed_image, langs='tel')
            confidence = len(text)
            if confidence > max_confidence:
                max_confidence = confidence
                best_text = text
        extracted_texts.append(best_text)
        return gr.update(value=best_text), next_page_num, gr.update(value=next_page_image, height=None, width=None), json_path
    else:
        return "All pages processed", page_num, None, json_path

def skip_page(page_num, extracted_texts, original_images, total_pages):
    next_page_num = int(page_num) + 1  # Ensure page_num is an integer and increment to next page
    if next_page_num <= total_pages:
        next_page_image = original_images[next_page_num - 1]
        methods = ['default', 'adaptive_threshold', 'edge_detection', 'morphological']
        best_text = ""
        max_confidence = -1
        for method in methods:
            processed_image = process_image(next_page_image, method=method)
            text = extract_text_from_image(processed_image, langs='tel')
            confidence = len(text)
            if confidence > max_confidence:
                max_confidence = confidence
                best_text = text
        extracted_texts.append(best_text)
        return gr.update(value=best_text), next_page_num, gr.update(value=next_page_image, height=None, width=None)
    else:
        return "All pages processed", page_num, None

def upload_pdf(pdf):
    pdf_path = pdf.name
    pages = convert_from_path(pdf_path)
    first_page = np.array(pages[0])
    methods = ['default', 'adaptive_threshold', 'edge_detection', 'morphological']
    best_text = ""
    max_confidence = -1
    for method in methods:
        processed_image = process_image(first_page, method=method)
        text = extract_text_from_image(processed_image, langs='tel')
        confidence = len(text)
        if confidence > max_confidence:
            max_confidence = confidence
            best_text = text
    original_images = [np.array(page) for page in pages]
    extracted_texts = [best_text]
    return gr.update(value=original_images[0], height=None, width=None), gr.update(value=best_text), 1, extracted_texts, original_images, len(pages)

def navigate_to_page(page_num, extracted_texts, original_images):
    if 0 <= page_num - 1 < len(original_images):
        return gr.update(value=original_images[page_num - 1], height=None, width=None), gr.update(value=extracted_texts[page_num - 1]), page_num
    else:
        return gr.update(value="Invalid Page Number"), None, page_num

def display_pdf_and_text():
    with gr.Blocks() as demo:
        gr.Markdown("## PDF Viewer and Text Editor")
        pdf_input = gr.File(label="Upload PDF", file_types=[".pdf"])
        with gr.Row():
            image_output = gr.Image(label="Page Image", type="numpy")
            text_editor = gr.Textbox(label="Extracted Text", lines=10, interactive=True)
        page_num = gr.Number(value=1, label="Page Number", visible=True)
        extracted_texts = gr.State()
        original_images = gr.State()
        total_pages = gr.State()
        save_next_button = gr.Button("Save and Next")
        skip_button = gr.Button("Skip")
        pdf_input.upload(upload_pdf, inputs=pdf_input, outputs=[image_output, text_editor, page_num, extracted_texts, original_images, total_pages])

        save_next_button.click(fn=save_and_next,
                               inputs=[page_num, text_editor, extracted_texts, original_images, total_pages],
                               outputs=[text_editor, page_num, image_output, gr.File(label="Download JSON")])

        skip_button.click(fn=skip_page,
                          inputs=[page_num, extracted_texts, original_images, total_pages],
                          outputs=[text_editor, page_num, image_output])

        page_buttons = gr.Row()

        def update_page_buttons(total_pages, extracted_texts, original_images):
            page_buttons.clear()  # Clear previous buttons if any
            buttons = []
            for i in range(1, total_pages + 1):
                button = gr.Button(str(i), variant="primary", size="small")
                button.click(navigate_to_page, inputs=[i, extracted_texts, original_images], outputs=[image_output, text_editor, page_num])
                buttons.append(button)
            return buttons

        total_pages.change(fn=update_page_buttons, inputs=[total_pages, extracted_texts, original_images], outputs=[page_buttons])

    return demo

iface = display_pdf_and_text()
iface.launch()