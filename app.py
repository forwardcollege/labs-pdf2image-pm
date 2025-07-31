import streamlit as st
import tempfile
import os
import base64
from PIL import Image
import io
from datetime import datetime
from utils.image_processor import PDFImageProcessor

@st.cache_resource
def get_processor():
    """Cached function to initialize and reuse the PDFImageProcessor."""
    return PDFImageProcessor()

def main():
    st.title("PM's PDF to Banner Image Generator")
    st.markdown("Upload the magazine PDF to generate the social sharing and cover image.")
    
    # Initialize the processor using the cached function
    processor = get_processor()

    # Initialize session state for generated images
    if 'img_bytes' not in st.session_state:
        st.session_state.img_bytes = None
    if 'cover_bytes' not in st.session_state:
        st.session_state.cover_bytes = None
    if 'uploaded_filename' not in st.session_state:
        st.session_state.uploaded_filename = None
    if 'cover_filename' not in st.session_state:
        st.session_state.cover_filename = None

    # File upload section
    st.header("Upload PDF File")
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=['pdf'],
        help="Upload a PDF file to extract the first page and create a banner image"
    )
    
    if uploaded_file is not None:
        # If a new file is uploaded, clear the previous state to avoid showing old results
        if uploaded_file.name != st.session_state.uploaded_filename:
            st.session_state.img_bytes = None
            st.session_state.cover_bytes = None
            st.session_state.uploaded_filename = uploaded_file.name
            st.session_state.cover_filename = None
            
        # Display file info
        st.success(f"✅ File uploaded: {uploaded_file.name} ({uploaded_file.size} bytes)")
        
        # Generate button
        if st.button("Generate Banner Image", type="primary"):
            try:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(uploaded_file.getbuffer())
                    pdf_path = tmp_file.name
                
                jpeg_path, final_image_path = None, None
                
                try:
                    status_text.text("Converting PDF to image...")
                    progress_bar.progress(40)
                    jpeg_path = processor.pdf_to_jpeg(pdf_path)
                    
                    status_text.text("Applying background and scaling...")
                    progress_bar.progress(70)
                    final_image_path = processor.center_and_fit_image_with_padding(jpeg_path, "assets/banner_bg.jpg")
                    
                    status_text.text("Finalizing image...")
                    progress_bar.progress(90)
                    
                    with open(final_image_path, 'rb') as img_file:
                        st.session_state.img_bytes = img_file.read()
                    
                    with open(jpeg_path, 'rb') as cover_file:
                        st.session_state.cover_bytes = cover_file.read()
                    
                    current_date = datetime.now()
                    st.session_state.cover_filename = f"{current_date.strftime('%m_%Y')}_cover.jpg"
                    
                    progress_bar.progress(100)
                    status_text.text("✅ Image generated successfully!")
                    
                finally:
                    cleanup_files = [pdf_path]
                    if jpeg_path: cleanup_files.append(jpeg_path)
                    if final_image_path: cleanup_files.append(final_image_path)
                    processor.cleanup_temp_files(cleanup_files)
                    
            except Exception as e:
                st.error(f"❌ Error processing PDF: {str(e)}")
                st.info("Please ensure the PDF file is valid and not corrupted.")
                st.session_state.img_bytes = None # Clear state on error
                st.session_state.cover_bytes = None

    # Display results and download buttons if they exist in session state
    if st.session_state.img_bytes:
        st.header("Generated Banner Image")
        st.image(st.session_state.img_bytes, caption="Generated Banner Image", use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="Download Banner Image",
                data=st.session_state.img_bytes,
                file_name=f"banner_{st.session_state.uploaded_filename.replace('.pdf', '.jpg')}",
                mime="image/jpeg",
                use_container_width=True
            )
        with col2:
            st.download_button(
                label="Download Cover Only",
                data=st.session_state.cover_bytes,
                file_name=st.session_state.cover_filename,
                mime="image/jpeg",
                use_container_width=True
            )
            
    elif uploaded_file is None:
        st.info("👆 Please upload a PDF file to get started.")

    # Instructions section
    with st.expander("ℹ️ How it works"):
        st.markdown("""
        1. **Upload** a PDF file using the file uploader above
        2. **Click** the "Generate Banner Image" button
        3. The app will:
           - Extract the first page of your PDF
           - Convert it to an image
           - Scale and center it on the background
           - Apply appropriate padding for a professional look
        4. **Download** your generated banner image
        
        **Note:** The generated image maintains the aspect ratio of your PDF page while fitting it proportionally within the banner background.
        """)

if __name__ == "__main__":
    main()
