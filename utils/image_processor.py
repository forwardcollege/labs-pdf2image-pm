import os
import tempfile
import fitz  # PyMuPDF
from PIL import Image

class PDFImageProcessor:
    """Handles PDF to image conversion and background processing using PyMuPDF"""
    
    def __init__(self):
        self.temp_files = []
    
    def pdf_to_jpeg(self, pdf_path):
        """
        Convert the first page of a PDF to JPEG format using PyMuPDF
        
        Args:
            pdf_path (str): Path to the input PDF file
            
        Returns:
            str: Path to the generated JPEG file
        """
        try:
            # Open the PDF with PyMuPDF
            doc = fitz.open(pdf_path)
            
            if not doc or doc.page_count == 0:
                raise ValueError("No pages found in PDF or PDF could not be processed")
            
            # Get the first page
            page = doc.load_page(0)
            
            # Render the page to a pixmap (image)
            pix = page.get_pixmap(dpi=300)  # Higher DPI for better quality
            
            # Convert the pixmap to a PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # Create temporary file for JPEG output
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                jpeg_output_path = tmp_file.name
            
            # Save the image as JPEG
            img.save(jpeg_output_path, 'JPEG', quality=95)
            self.temp_files.append(jpeg_output_path)
            
            doc.close()
            
            return jpeg_output_path
            
        except Exception as e:
            raise Exception(f"Failed to convert PDF to JPEG: {str(e)}")
    
    def center_and_fit_image_with_padding(self, jpeg_path, background_path, padding_ratio=0.9):
        """
        Center and fit an image on a background with padding
        
        Args:
            jpeg_path (str): Path to the JPEG image to be placed
            background_path (str): Path to the background image
            padding_ratio (float): Ratio for padding (0.9 = 10% padding)
            
        Returns:
            str: Path to the final output image
        """
        try:
            # Open the JPEG (first page of the PDF)
            jpeg = Image.open(jpeg_path)
            
            # Open the background image
            if not os.path.exists(background_path):
                raise FileNotFoundError(f"Background image not found: {background_path}")
            
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
            
            # Create a copy of the background to avoid modifying the original
            final_image = background.copy()
            
            # Paste the resized JPEG onto the background
            final_image.paste(jpeg_resized, (x_offset, y_offset))
            
            # Create temporary file for final output
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                final_output_path = tmp_file.name
            
            # Save the final image
            final_image.save(final_output_path, 'JPEG', quality=95)
            self.temp_files.append(final_output_path)
            
            return final_output_path
            
        except Exception as e:
            raise Exception(f"Failed to process image: {str(e)}")
    
    def cleanup_temp_files(self, additional_files=None):
        """
        Clean up temporary files created during processing
        
        Args:
            additional_files (list): Additional file paths to clean up
        """
        files_to_clean = self.temp_files.copy()
        if additional_files:
            files_to_clean.extend(additional_files)
        
        for file_path in files_to_clean:
            try:
                if os.path.exists(file_path):
                    os.unlink(file_path)
            except Exception as e:
                # Log error but don't raise - cleanup should be non-blocking
                print(f"Warning: Could not clean up temporary file {file_path}: {e}")
        
        self.temp_files.clear()
