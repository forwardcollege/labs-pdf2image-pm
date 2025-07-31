# PM's PDF to Banner Image Generator

## Overview

This is a Streamlit web application that converts magazine PDF files into social sharing and cover images by extracting the first page of a PDF and superimposing it on a background image. The application provides a simple web interface for users to upload magazine PDF files and generate professional-looking banner and cover images.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a simple web-based architecture with the following layers:

1. **Frontend**: Streamlit web interface for file upload and user interaction
2. **Processing Layer**: Custom image processing utilities for PDF conversion and image manipulation
3. **File System**: Temporary file storage for processing uploaded files

The architecture is designed for simplicity and ease of deployment, making it suitable for single-user or small-scale usage scenarios.

## Key Components

### Frontend (app.py)
- **Streamlit Application**: Main entry point providing a web interface
- **File Upload Handler**: Manages PDF file uploads with validation
- **Progress Tracking**: Real-time feedback during processing operations
- **Results Display**: Shows generated banner images to users

### Image Processing (utils/image_processor.py)
- **PDFImageProcessor Class**: Core processing engine with the following capabilities:
  - PDF to JPEG conversion using pdf2image library
  - Image scaling and centering with configurable padding
  - Temporary file management for cleanup
  - Error handling and validation

### Legacy Code (attached_assets/)
- Contains original standalone script that demonstrates the core functionality
- Serves as reference implementation for the processing logic

## Data Flow

1. **File Upload**: User uploads PDF file through Streamlit interface
2. **Temporary Storage**: PDF is saved to temporary file system location
3. **PDF Conversion**: First page extracted and converted to JPEG format
4. **Image Processing**: JPEG is scaled, centered, and composited with background
5. **Result Display**: Final banner image is presented to user
6. **Cleanup**: Temporary files are managed and cleaned up

## External Dependencies

### Core Libraries
- **Streamlit**: Web application framework for the user interface
- **pdf2image**: PDF to image conversion (requires poppler-utils system dependency)
- **Pillow (PIL)**: Image manipulation and processing
- **tempfile**: Temporary file management
- **base64**: File encoding for web display

### System Dependencies
- **poppler-utils**: Required by pdf2image for PDF rendering
- **Python 3.x**: Runtime environment

## Deployment Strategy

The application is designed for simple deployment scenarios:

1. **Local Development**: Can be run locally using `streamlit run app.py`
2. **Cloud Platforms**: Compatible with Streamlit Cloud, Heroku, or similar platforms
3. **Docker**: Can be containerized with appropriate system dependencies
4. **Replit**: Suitable for deployment on Replit with package management

### Key Deployment Considerations
- Ensure poppler-utils is installed in the deployment environment
- Configure appropriate file upload limits for expected PDF sizes
- Set up proper error handling for memory constraints with large PDFs
- Consider implementing file cleanup mechanisms for production use

### Security Notes
- Application uses temporary files which are cleaned up after processing
- No persistent storage of user files
- Input validation limited to file type checking
- Consider adding file size limits for production deployment