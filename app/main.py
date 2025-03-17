from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from .models import StoryRequest, StoryResponse
from .story_generator import generate_story
from .config import STATIC_DIR
from .logger import logger
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
        logger.debug(f"Parameters - Chapters: {request.num_chapters}, Words per chapter: {request.words_per_chapter}")
        
        result = generate_story(
            theme=request.theme,
            num_chapters=request.num_chapters,
            words_per_chapter=request.words_per_chapter
        )
        
        if not result:
            logger.error("Story generation failed - no result returned")
            raise HTTPException(
                status_code=500,
                detail="Failed to generate story"
            )

        # Verify file exists
        if not os.path.exists(result):
            logger.error(f"Generated PDF file not found at: {result}")
            raise HTTPException(
                status_code=500,
                detail="Generated PDF file not found"
            )
        
        # Get the relative path from STATIC_DIR
        try:
            rel_path = os.path.relpath(result, STATIC_DIR)
            pdf_url = f"/static/{rel_path.replace(os.sep, '/')}"
            
            logger.info(f"Story generated successfully - File: {result}")
            logger.debug(f"PDF URL: {pdf_url}")
            
            return StoryResponse(
                pdf_url=pdf_url,
                message="Story generated successfully"
            )
        except Exception as path_error:
            logger.error(f"Error processing file path: {str(path_error)}")
            # Return the successful response even if path processing fails
            return StoryResponse(
                pdf_url=f"/static/CuentosGenerados/{os.path.basename(result)}",
                message="Story generated successfully (path processing warning)"
            )
    
    except Exception as e:
        logger.exception("Error during story generation")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating story: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)