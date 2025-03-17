from pydantic import BaseModel, Field

class StoryRequest(BaseModel):
    theme: str = Field(..., description="Theme of the story")
    num_chapters: int = Field(..., ge=1, le=10, description="Number of chapters")
    words_per_chapter: int = Field(..., ge=50, le=500, description="Words per chapter")

class StoryResponse(BaseModel):
    pdf_url: str = Field(..., description="URL to access the generated PDF")
    message: str = Field(..., description="Status message")