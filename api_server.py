from typing import List

from fastapi import FastAPI, File, UploadFile

app = FastAPI()

# Endpoint to retrieve available presentation slide templates
@app.get("/presentation/slides")
def get_slide_templates():
    # Your implementation here
    slide_templates = [
        {
            "id": 1,
            "name": "Template 1",
            "description": "This is template 1",
        },
        {
            "id": 2,
            "name": "Template 2",
            "description": "This is template 2",
        },
        {
            "id": 3,
            "name": "Template 3",
            "description": "This is template 3",
        },
    ]
    return slide_templates


# Endpoint to retrieve details of a specific slide template
@app.get("/presentation/slides/{slide_id}")
def get_slide_template(slide_id: int):
    # Your implementation here
    slide_template = {
        "id": slide_id,
        "name": f"Template {slide_id}",
        "description": f"This is template {slide_id}",
    }
    return slide_template


# Endpoint to combine selected presentation slides into a new presentation
@app.post("/presentation/combine")
def combine_slides(selected_slides: list[str]):
    # Your implementation here
    combined_presentation = {
        "selected_slides": selected_slides,
        "message": "Combined presentation created successfully",
    }
    return combined_presentation


# Endpoint to retrieve presentation files stored in Google Cloud Storage
@app.get("/presentation/files")
def get_presentation_files():
    # Your implementation here
    presentation_files = [
        "file1.pptx",
        "file2.pptx",
        "file3.pptx",
    ]
    return presentation_files


# Endpoint to change colors in the presentation
@app.post("/presentation/color")
def change_colors(color_data: dict):
    # Your implementation here
    changed_colors = {
        "color_data": color_data,
        "message": "Colors changed successfully",
    }
    return changed_colors


# Endpoint to retrieve the current color scheme used in the presentation
@app.get("/presentation/colors")
def get_color_scheme():
    # Your implementation here
    color_scheme = {
        "main_color": "#FF0000",
        "sub_color1": "#00FF00",
        "sub_color2": "#0000FF",
    }
    return color_scheme


# Endpoint to update the color scheme with the user's chosen colors
@app.put("/presentation/colors")
def update_color_scheme(color_data: dict):
    # Your implementation here
    updated_color_scheme = {
        "color_data": color_data,
        "message": "Color scheme updated successfully",
    }
    return updated_color_scheme


# Endpoint to upload the final presentation to Google Drive
@app.post("/presentation/upload")
def upload_presentation(file: UploadFile = File(...)):
    # Your implementation here
    file_data = {
        "filename": file.filename,
        "message": "Presentation uploaded successfully",
    }
    return file_data
