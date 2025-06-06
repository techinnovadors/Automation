import pytesseract
from pdf2image import convert_from_path
import os
from pathlib import Path
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import json
import time
from typing import Dict, List, Tuple
import logging
from fastapi import UploadFile
import tempfile
import shutil

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("uvicorn")


def process_page(args: Tuple[int, bytes]) -> Dict:
    """
    Process a single page of the PDF using OCR.
    Returns a dictionary with page number and extracted text.
    """
    page_num, image = args
    try:
        # Configure Tesseract parameters for better accuracy
        custom_config = r"--oem 3 --psm 6"
        text = pytesseract.image_to_string(image, config=custom_config)

        return {"page_number": page_num + 1, "text": text.strip(), "status": "success"}
    except Exception as e:
        logger.error(f"Error processing page {page_num + 1}: {str(e)}")
        return {
            "page_number": page_num + 1,
            "text": "",
            "status": "error",
            "error": str(e),
        }


def process_scanned_pdf(pdf_path: str, output_dir: str = None) -> Dict:
    """
    Process a scanned PDF file using OCR to extract text content efficiently.
    """
    start_time = time.time()
    logger.info(f"Processing scanned PDF: {pdf_path}")

    try:
        # Convert PDF to images with optimized settings
        logger.info("Converting PDF to images...")
        images = convert_from_path(
            pdf_path,
            dpi=300,  # Optimize DPI for better quality
            thread_count=cpu_count(),  # Use all available CPU cores
            grayscale=True,  # Convert to grayscale for better OCR
        )

        total_pages = len(images)
        logger.info(f"Total pages to process: {total_pages}")

        # Process pages in parallel
        with Pool(processes=cpu_count()) as pool:
            results = list(
                tqdm(
                    pool.imap(process_page, enumerate(images)),
                    total=total_pages,
                    desc="Processing pages",
                )
            )

        # Compile results
        processed_data = {
            "metadata": {
                "filename": os.path.basename(pdf_path),
                "total_pages": total_pages,
                "processing_time": time.time() - start_time,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            },
            "pages": results,
        }

        # Save results if output directory is provided
        if output_dir:
            output_path = Path(output_dir) / f"{Path(pdf_path).stem}_processed.json"
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(processed_data, f, ensure_ascii=False, indent=2)
            logger.info(f"Results saved to: {output_path}")

        return processed_data

    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")
        raise


async def process_uploaded_pdf(file: UploadFile) -> str:
    """
    Process an uploaded PDF file and return the combined text content.

    Args:
        file (UploadFile): The uploaded PDF file from FastAPI

    Returns:
        str: Combined text content from all pages
    """
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Save the uploaded file temporarily
            temp_file_path = Path(temp_dir) / file.filename
            with open(temp_file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # Process the PDF
            results = process_scanned_pdf(str(temp_file_path))

            # Combine text from all pages
            full_text = "\n\n".join(
                page["text"] for page in results["pages"] if page["status"] == "success"
            )

            return full_text

        except Exception as e:
            logger.error(f"Error processing uploaded PDF: {str(e)}")
            raise
        finally:
            # Ensure the file is closed
            await file.close()


if __name__ == "__main__":
    # Get the current directory
    current_dir = Path(__file__).parent

    # PDF file path
    pdf_path = current_dir / "TMIPL FY 2022-23_Standalone FS (1).pdf"

    if pdf_path.exists():
        try:
            # Create output directory if it doesn't exist
            output_dir = current_dir / "processed_output"
            output_dir.mkdir(exist_ok=True)

            # Process the PDF
            results = process_scanned_pdf(str(pdf_path), str(output_dir))

            # Print summary
            print("\nProcessing Summary:")
            print(f"Total pages processed: {results['metadata']['total_pages']}")
            print(
                f"Processing time: {results['metadata']['processing_time']:.2f} seconds"
            )
            print(
                f"Successful pages: {sum(1 for page in results['pages'] if page['status'] == 'success')}"
            )
            print(
                f"Failed pages: {sum(1 for page in results['pages'] if page['status'] == 'error')}"
            )

        except Exception as e:
            logger.error(f"Failed to process PDF: {str(e)}")
    else:
        logger.error(f"PDF file not found at: {pdf_path}")
