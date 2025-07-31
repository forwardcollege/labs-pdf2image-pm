from pdf2image import convert_from_path
from PIL import Image

def pdf_to_jpeg(pdf_path, jpeg_output_path):
    # Convert the first page of the PDF to an image
    images = convert_from_path(pdf_path, first_page=1, last_page=1)
    # Save the first page as JPEG
    images[0].save(jpeg_output_path, 'JPEG')
    print(f"Saved first page as {jpeg_output_path}")

def center_and_fit_image_with_padding(jpeg_path, background_path, output_path, padding_ratio=0.9):
    # Open the JPEG (first page of the PDF)
    jpeg = Image.open(jpeg_path)
    
    # Open the background image
    background = Image.open(background_path)

    # Resize the JPEG proportionally to fit within the background dimensions with padding
    bg_width, bg_height = background.size
    jpeg_width, jpeg_height = jpeg.size

    # Calculate scaling factor to fit the JPEG into the background, including padding
    scale = min(bg_width / jpeg_width, bg_height / jpeg_height) * padding_ratio
    new_width = int(jpeg_width * scale)
    new_height = int(jpeg_height * scale)
    jpeg_resized = jpeg.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Calculate position to center the resized JPEG on the background
    x_offset = (bg_width - new_width) // 2
    y_offset = (bg_height - new_height) // 2

    # Paste the resized JPEG onto the background
    background.paste(jpeg_resized, (x_offset, y_offset))

    # Save the final image
    background.save(output_path, 'JPEG')
    print(f"Saved centered and scaled image with padding as {output_path}")

# Input paths
pdf_path = "PM_Digital.pdf"          # Input PDF file
background_path = "Banner_BG_Only.jpg"      # Background image
jpeg_output_path = "first-page.jpg"     # Intermediate JPEG output
final_output_path = "final-output.jpg"  # Final output

# Step 1: Extract the first page of the PDF as JPEG
pdf_to_jpeg(pdf_path, jpeg_output_path)

# Step 2: Fit the JPEG proportionally into the background and center it with padding
center_and_fit_image_with_padding(jpeg_output_path, background_path, final_output_path)