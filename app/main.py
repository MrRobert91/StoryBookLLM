from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from .models import StoryRequest, StoryResponse
from .story_generator import generate_story
from .config import STATIC_DIR
import os
import uvicorn

app = FastAPI(
    title="StoryBook API",
    description="API for generating children's stories using LLM",
    version="1.0.0"
)

# Mount static directory for serving PDFs
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.post("/api/generate-story", response_model=StoryResponse)
async def create_story(request: StoryRequest):
    try:
        result = generate_story(
            theme=request.theme,
            num_chapters=request.num_chapters,
            words_per_chapter=request.words_per_chapter
        )
        
        if not result:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate story"
            )

        try:
            # Verify file exists
            if not os.path.exists(result):
                raise HTTPException(
                    status_code=500,
                    detail="Generated PDF file not found"
                )
            
            # Get just the filename from the full path
            pdf_filename = os.path.basename(result)
            # Create the correct URL path
            pdf_url = f"/static/CuentosGenerados/{pdf_filename}"
            
            print(f"File path: {result}")
            print(f"PDF URL: {pdf_url}")
            
            return StoryResponse(
                pdf_url=pdf_url,
                message="Story generated successfully"
            )
            
        except Exception as path_error:
            raise HTTPException(
                status_code=500,
                detail=f"Error processing PDF path: {str(path_error)}"
            )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating story: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)