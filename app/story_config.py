class PDFStyle:
    def __init__(self):
# Simple color scheme
        self.color_scheme = {
            'primary': '#000000',    # Blue - 333333Dark gray for headings
            'secondary': '#000000',   # Medium gray for subheadings
            'accent': '#e74c3c',      # Black for accents
            'background': '#ffffff',  # White background
            'text': '#000000'        # Dark gray for text
        }
        
        self.fonts = {
            'main': 'Arial',
            'title': 'Arial',
            'heading': 'Arial',
            'body': 'Arial'
        }
        
        self.sizes = {
            'title': '24pt',
            'chapter': '18pt',
            'body': '12pt',
            'spacing': '1.5'
        }

class StoryConfig:
    _instance = None  # Singleton instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._theme = "universo fractal"
            self._num_chapters = 5
            self._words_per_chapter = 50
            self._initialized = True
            self._pdf_style = PDFStyle()
            print(f"StoryConfig initialized with theme: {self._theme}")

    @property
    def theme(self):
        return self._theme

    @theme.setter
    def theme(self, value):
        if value and isinstance(value, str):
            print(f"Updating theme from '{self._theme}' to '{value}'")
            self._theme = value

    @property
    def num_chapters(self):
        return self._num_chapters

    @num_chapters.setter
    def num_chapters(self, value):
        if value and isinstance(value, int):
            self._num_chapters = value
            print(f"Chapters updated to: {self._num_chapters}")

    @property
    def words_per_chapter(self):
        return self._words_per_chapter

    @words_per_chapter.setter
    def words_per_chapter(self, value):
        if value and isinstance(value, int):
            self._words_per_chapter = value
            print(f"Words per chapter updated to: {self._words_per_chapter}")

    @property
    def pdf_style(self):
        return self._pdf_style

# Create a global instance
story_config = StoryConfig()

# Explicitly define what can be imported
__all__ = ['StoryConfig', 'PDFStyle', 'story_config']

# Make sure the class is available at module level
globals()['StoryConfig'] = StoryConfig