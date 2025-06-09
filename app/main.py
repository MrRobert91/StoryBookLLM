from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from app.models import StoryRequest, StoryResponse  # Changed from relative import
from app.story_generator import generate_story      # Changed from relative import
from app.config import STATIC_DIR, CUENTOS_DIR      # Changed from relative import
from app.logger import logger                      # Changed from relative import
import os
import uvicorn

app = FastAPI(
    title="StoryBook API",
    description="API for generating children's stories using LLM",
    version="1.0.0"
)

# Mount static directory for serving PDFs
logger.info(f"Mounting static directory: {STATIC_DIR}")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.post("/api/generate-story", response_model=StoryResponse)
async def create_story(request: StoryRequest):
    """
    Generate a story based on the provided theme and parameters
    """
    try:
        logger.info(f"Starting story generation with theme: {request.theme}")
        
        # Generate story returns both pdf_path and crew result
        pdf_path, crew_result = generate_story(
            theme=request.theme,
            num_chapters=request.num_chapters,
            words_per_chapter=request.words_per_chapter
        )
        
        if not pdf_path:
            logger.error("Story generation failed - no PDF path returned")
            raise HTTPException(
                status_code=500,
                detail="Failed to generate story"
            )

        logger.debug(f"Checking PDF at path: {pdf_path}")
        if not os.path.exists(pdf_path):
            logger.error(f"Generated PDF file not found at: {pdf_path}")
            raise HTTPException(
                status_code=500,
                detail="Generated PDF file not found"
            )
        
        # Convert absolute path to relative URL path for client
        relative_path = os.path.relpath(pdf_path, STATIC_DIR)
        pdf_url = f"/static/{relative_path.replace(os.sep, '/')}"

        logger.info(f"Story generated successfully at: {pdf_url}")
        return StoryResponse(
            pdf_url=pdf_url,
            message="Story generated successfully"
        )
    
    except Exception as e:
        logger.exception("Error during story generation")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating story: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)