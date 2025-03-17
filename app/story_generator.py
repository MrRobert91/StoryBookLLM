from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import tool, DallETool
from langchain_openai import ChatOpenAI
from crewai_tools.tools import FileReadTool
import os, requests, re, mdpdf, subprocess
from weasyprint import HTML
from openai import OpenAI
from datetime import datetime
from spire.doc import *
from spire.doc.common import *
import markdown2
from markdown_pdf import MarkdownPdf, Section
from pdf_styles import PDFStyle
from .story_config import StoryConfig
from .config import CUENTOS_DIR
from .logger import logger

'''

# Load environment variables
load_dotenv()

# Environment variables
LANGCHAIN_TRACING_V2 = os.getenv('LANGCHAIN_TRACING_V2')
LANGCHAIN_API_KEY = os.getenv('LANGCHAIN_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")
CUENTOS_DIR = os.path.join(STATIC_DIR, "CuentosGenerados")

# Create necessary directories
os.makedirs(CUENTOS_DIR, exist_ok=True)
'''

# Add these configurations at the beginning of the file, after the environment variables
'''


# Story Configuration
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
'''


# Create a global config instance
story_config = StoryConfig()

def configure_story(theme=None, num_chapters=None, words_per_chapter=None):
    """
    Configure story parameters
    Args:
        theme (str): Theme of the story
        num_chapters (int): Number of chapters
        words_per_chapter (int): Words per chapter
    """
    print("\n=== Configuring Story ===")
    print(f"Current theme: {story_config.theme}")
    print(f"New theme requested: {theme}")
    
    if theme is not None:
        story_config.theme = theme
    if num_chapters is not None:
        story_config.num_chapters = num_chapters
    if words_per_chapter is not None:
        story_config.words_per_chapter = words_per_chapter
    
    print(f"Final theme: {story_config.theme}")
    return story_config

def create_story_folder(theme):
    """
    Creates a folder structure for storing story files
    Returns the path to the new story folder
    """
    def sanitize_filename(filename):
        clean_name = re.sub(r'[^a-zA-Z0-9]', '_', filename)
        return clean_name[:50]

    base_folder = "CuentosGenerados"
    date_now = datetime.now().strftime("%Y%m%d_%H%M%S")
    sanitized_theme = sanitize_filename(theme)
    story_folder = f"{sanitized_theme}_{date_now}"
    full_path = os.path.join(os.getcwd(), base_folder, story_folder)
    
    os.makedirs(full_path, exist_ok=True)
    
    return full_path

llm = ChatOpenAI(
    openai_api_base="https://api.openai.com/v1", # https://api.openai.com/v1 or https://api.groq.com/openai/v1 
    openai_api_key=os.getenv("OPENAI_API_KEY"), # os.getenv("OPENAI_API_KEY") or os.getenv("GROQ_API_KEY")
    model_name="openai/gpt-4o-mini" #  GPT-4o-mini or groq/llama-3.3-70b-versatile
)

file_read_tool = FileReadTool(
	file_path='template.md',
	description='A tool to read the Story Template file and understand the expected output format.'
)




dalle_tool = DallETool(model="dall-e-3",
                       size="1024x1024",
                       quality="standard",
                       n=1)

'''


@tool
def generateimageold(chapter_content_and_character_details: str) -> str:
    """
    Generates an image for a given chapter number, chapter content, detailed location details and character details.
    Using the OpenAI image generation API,
    saves it in the current folder, and returns the image path.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    print("----chapter_content_and_character_details: ----")
    print(type(chapter_content_and_character_details))
    print(chapter_content_and_character_details)

    #dict

    #dalle_prompt = f"Image is about: {chapter_content_and_character_details["description"]}. Style: Illustration. Create an illustration incorporating a vivid palette with an emphasis on shades of azure and emerald, augmented by splashes of gold for contrast and visual interest. The style should evoke the intricate detail and whimsy of early 20th-century storybook illustrations, blending realism with fantastical elements to create a sense of wonder and enchantment. The composition should be rich in texture, with a soft, luminous lighting that enhances the magical atmosphere. Attention to the interplay of light and shadow will add depth and dimensionality, inviting the viewer to delve into the scene. DON'T include ANY text in this image. DON'T include colour palettes in this image."
    dalle_prompt = f"Image is about: {chapter_content_and_character_details}. Style: Illustration. Create an illustration incorporating a vivid palette with an emphasis on shades of azure and emerald, augmented by splashes of gold for contrast and visual interest. The style should evoke the intricate detail and whimsy of early 20th-century storybook illustrations, blending realism with fantastical elements to create a sense of wonder and enchantment. The composition should be rich in texture, with a soft, luminous lighting that enhances the magical atmosphere. Attention to the interplay of light and shadow will add depth and dimensionality, inviting the viewer to delve into the scene. DON'T include ANY text in this image. DON'T include colour palettes in this image."

    print("--- dalle_prompt ----")
    print(dalle_prompt)

    response = client.images.generate(
        model="dall-e-3",
        prompt=str(dalle_prompt),
        size="1024x1024",
        quality="standard",
        n=1,
    )
    
    image_url = response.data[0].url
    words = chapter_content_and_character_details.split()[:5] 
    safe_words = [re.sub(r'[^a-zA-Z0-9_]', '', word) for word in words]  
    filename = "_".join(safe_words).lower() + ".png"
    filepath = os.path.join(os.getcwd(), filename)

    # Download the image from the URL
    image_response = requests.get(image_url)
    if image_response.status_code == 200:
        with open(filepath, 'wb') as file:
            file.write(image_response.content)
    else:
        print("Failed to download the image.")
        return ""

    return filepath
'''

@tool
def generateimage(prompt: str | dict) -> str:
    """
    Generates an image and saves it in a theme-specific folder within static/ImagenesGeneradas
    """
    try:
        from openai import OpenAI
        import os
        import requests
        from datetime import datetime
        import re
        from .config import IMAGENES_DIR

        logger.info("Starting image generation")
        logger.debug(f"Image prompt: {prompt}")

        # Process prompt if it's a dictionary
        if isinstance(prompt, dict):
            # Extract relevant information from the dictionary
            prompt_text = prompt.get('description', '') if 'description' in prompt else str(prompt)
        else:
            prompt_text = str(prompt)

        # Add style guidelines to the prompt
        dalle_prompt = f"""Image is about: {prompt_text}. 
        Style: Illustration. Create an illustration incorporating a vivid palette 
        with an emphasis on shades of azure and emerald, augmented by splashes 
        of gold for contrast and visual interest. The style should evoke the 
        intricate detail and whimsy of early 20th-century storybook illustrations, 
        blending realism with fantastical elements. DON'T include ANY text or 
        colour palettes in this image."""

        # Create theme-specific directory name
        date_now = datetime.now().strftime("%Y%m%d_%H%M%S")
        sanitized_theme = re.sub(r'[^a-zA-Z0-9]', '_', story_config.theme)[:30]
        theme_folder_name = f"cuento_{sanitized_theme}_{date_now}"
        
        # Create full path for theme-specific image folder
        theme_image_dir = os.path.join(IMAGENES_DIR, theme_folder_name)
        os.makedirs(theme_image_dir, exist_ok=True)
        
        # Create image filename
        sanitized_prompt = re.sub(r'[^a-zA-Z0-9]', '_', prompt_text[:30])
        image_filename = f"imagen_{sanitized_prompt}_{date_now}.png"
        output_file = os.path.join(theme_image_dir, image_filename)
        
        print(f"Generating image at: {output_file}")
        print(f"Using prompt: {dalle_prompt[:200]}...")

        # Generate image using OpenAI
        client = OpenAI()
        response = client.images.generate(
            model="dall-e-3",
            prompt=dalle_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        # Download and save image
        image_url = response.data[0].url
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(output_file, 'wb') as f:
                f.write(response.content)
            logger.info(f"Image generated successfully at: {output_file}")
            return output_file
        else:
            print("Failed to download image")
            return ""

    except Exception as e:
        logger.exception("Error during image generation")
        return ""

@tool
def convermarkdowntopdf(markdownfile_name: str) -> str:
    """
    Converts a Markdown file to a PDF document and saves it in the static/CuentosGenerados folder
    """
    try:
        from xhtml2pdf import pisa
        import markdown2
        from bs4 import BeautifulSoup
        import base64
        from datetime import datetime
        import os
        from .config import CUENTOS_DIR  # Import the correct path from config
        import re

        logger.info(f"Starting PDF conversion for: {markdownfile_name}")

        # Verify input file exists
        if not os.path.exists(markdownfile_name):
            print(f"Error: Markdown file not found - {markdownfile_name}")
            return ""

        # Create sanitized filename
        date_now = datetime.now().strftime("%Y%m%d_%H%M%S")
        sanitized_theme = re.sub(r'[^a-zA-Z0-9]', '_', story_config.theme)[:30]
        pdf_filename = f"cuento_{sanitized_theme}_{date_now}.pdf"
        
        # Use CUENTOS_DIR for the output path
        output_file = os.path.join(CUENTOS_DIR, pdf_filename)
        
        print(f"Generating PDF at: {output_file}")

        # Convert markdown to HTML
        with open(markdownfile_name, 'r', encoding='utf-8') as md_file:
            html_content = markdown2.markdown(md_file.read())


        # CSS template using story_config.pdf_style values
        css = f"""
            @page {{ 
                size: A4; 
                margin: 2.5cm; 
            }}
            body {{ 
                font-family: {story_config.pdf_style.fonts['body']}, sans-serif; 
                font-size: {story_config.pdf_style.sizes['body']}; 
                line-height: {story_config.pdf_style.sizes['spacing']}; 
                color: {story_config.pdf_style.color_scheme['text']};
                background-color: {story_config.pdf_style.color_scheme['background']};
            }}
            h1 {{ 
                font-family: {story_config.pdf_style.fonts['title']}, serif;
                font-size: {story_config.pdf_style.sizes['title']};
                color: {story_config.pdf_style.color_scheme['primary']};
                text-align: center; 
                margin: 2cm 0 1cm 0;
                padding-bottom: 0.5cm;
            }}
            h2 {{ 
                font-family: {story_config.pdf_style.fonts['heading']}, sans-serif;
                font-size: {story_config.pdf_style.sizes['chapter']};
                color: {story_config.pdf_style.color_scheme['secondary']};
                page-break-before: always;
                margin-top: 1cm;
                padding-bottom: 0.3cm;
                border-bottom: 1px solid {story_config.pdf_style.color_scheme['accent']};
            }}
            img {{ 
                max-width: 80%; 
                display: block; 
                margin: 1cm auto;
                page-break-inside: avoid;
            }}
            p {{ 
                text-align: justify; 
                margin-bottom: 0.5cm;
                font-family: {story_config.pdf_style.fonts['body']}, sans-serif;
            }}
        """

        # Create complete HTML
        html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>{css}</style>
            </head>
            <body>{html_content}</body>
            </html>
        """

        # Ensure the output directory exists
        os.makedirs(CUENTOS_DIR, exist_ok=True)

        # Convert to PDF
        with open(output_file, "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(
                html,
                dest=pdf_file,
                encoding='utf-8'
            )

        if pisa_status.err:
            print("Error creating PDF")
            return ""

        logger.info(f"PDF generated successfully at: {output_file}")
        return output_file

    except Exception as e:
        logger.exception("Error during PDF conversion")
        return ""

# HElper function to convert markdown to pdf
def markdown_to_pdf(markdownfile_name, output_file):
        # Leer el contenido del archivo Markdown
        with open(markdownfile_name, 'r', encoding='utf-8') as md_file:
            markdown_content = md_file.read()

        # Convertir Markdown a HTML
        html_content = markdown2.markdown(markdown_content)

        # Generar el PDF desde el HTML
        HTML(string=html_content).write_pdf(output_file)

        print(f"PDF generado con éxito: {output_file}")

        return output_file

def create_agents_and_tasks():
    """
    Creates agents and tasks with current story configuration
    """
    story_outliner = Agent(
        role='Creador de Esquema',
        goal=f"Desarrollar un esquema para un libro infantil sobre {story_config.theme}, incluyendo títulos de capítulos y personajes para {story_config.num_chapters} capítulos.",
        backstory="Un creador imaginativo que establece las bases de historias cautivadoras para niños.",
        verbose=True,
        llm=llm,
        allow_delegation=False
    )

    story_writer = Agent(
        role='Escritor de Historia',
        goal=f'Escribir el contenido completo de la historia para los {story_config.num_chapters} capítulos, cada capítulo con {story_config.words_per_chapter} palabras, entrelazando las narrativas y los personajes descritos.',
        backstory="Un narrador talentoso que da vida al mundo y los personajes esbozados, creando cuentos imaginativos y atractivos para niños.",
        verbose=True,
        llm=llm,
        allow_delegation=False
    )

    image_generator = Agent(
        role='Generador de Imágenes',
        goal=f'Generar una imagen por cada contenido de capítulo proporcionado por el creador del esquema. Comenzar con el número del capítulo, contenido del capítulo, detalles de los personajes, información detallada de la ubicación y elementos detallados en el lugar donde ocurre la actividad. Generar un total de {story_config.num_chapters} imágenes una por una. La salida final debe contener todas las {story_config.num_chapters} imágenes en formato json.',
        backstory="Una IA creativa especializada en narración visual, dando vida a cada capítulo a través de imágenes imaginativas.",
        verbose=True,
        llm=llm,
        tools=[generateimage],
        allow_delegation=False
    )

    content_formatter = Agent(
        role='Formateador de Contenido',
        goal='Formatear el contenido escrito de la historia en markdown, incluyendo imágenes al principio de cada capítulo.',
        backstory='Un formateador meticuloso que mejora la legibilidad y presentación del libro de cuentos.',
        verbose=True,
        llm=llm,
        tools=[file_read_tool],
        allow_delegation=False
    )

    markdown_to_pdf_creator = Agent(
        role='Conversor a PDF',
        goal='Convertir el archivo Markdown a un documento PDF. story.md es el nombre del archivo markdown.',
        backstory='Un conversor eficiente que transforma archivos Markdown en documentos PDF profesionalmente formateados.',
        verbose=True,
        llm=llm,
        tools=[convermarkdowntopdf],
        allow_delegation=False
    )

    task_outline = Task(
        description=f"Crear un esquema para el libro infantil sobre {story_config.theme}, detallando títulos de capítulos y descripciones de personajes para {story_config.num_chapters} capítulos.",
        agent=story_outliner,
        expected_output=f'Un documento estructurado que contiene {story_config.num_chapters} títulos de capítulos, con descripciones detalladas de personajes y los puntos principales de la trama para cada capítulo.'
    )

    task_write = Task(
        description=f'Usando el esquema proporcionado, escribir el contenido completo de la historia para todos los capítulos, asegurando una narrativa cohesiva y atractiva para niños. Cada capítulo con {story_config.words_per_chapter} palabras. Incluir el título de la historia al principio.',
        agent=story_writer,
        expected_output=f"Un manuscrito completo del libro infantil sobre {story_config.theme} con {story_config.num_chapters} capítulos. Cada capítulo debe contener aproximadamente {story_config.words_per_chapter} palabras, siguiendo el esquema proporcionado e integrando los personajes y puntos de trama en una narrativa cohesiva."
    )

    task_image_generate = Task(
        description=f"Generar {story_config.num_chapters} imágenes que capturen la esencia del libro infantil sobre {story_config.theme}, alineándose con los temas, personajes y narrativa descritos para los capítulos. Hacerlo uno por uno.",
        agent=image_generator,
        expected_output=f'Un archivo de imagen digital que representa visualmente el tema general del libro infantil, incorporando elementos de los personajes y la trama según se describe en el esquema. La imagen debe ser adecuada para su inclusión en el libro como ilustración.',
    )

    task_format_content = Task(
        description='Formatear el contenido de la historia en markdown, incluyendo una imagen al principio de cada capítulo.',
        agent=content_formatter,
        expected_output='Todo el contenido del libro formateado en markdown, con cada título de capítulo seguido por la imagen correspondiente y el contenido del capítulo. Eliminar la sintaxis ```markdown de la salida',
        context=[task_write, task_image_generate],
        output_file="story.md"
    )

    task_markdown_to_pdf = Task(
        description='Convertir un archivo Markdown a un documento PDF, asegurando la preservación del formato, estructura e imágenes incrustadas usando la biblioteca mdpdf.',
        agent=markdown_to_pdf_creator,
        expected_output='Un archivo PDF generado desde el Markdown de entrada, reflejando con precisión el contenido con el formato adecuado. El PDF debe estar listo para compartir o imprimir.'
    )

    return {
        'agents': [story_outliner, story_writer, image_generator, content_formatter, markdown_to_pdf_creator],
        'tasks': [task_outline, task_write, task_image_generate, task_format_content, task_markdown_to_pdf]
    }

def generate_story(theme=None, num_chapters=None, words_per_chapter=None):
    """
    Generate a story with custom parameters and organize files in a dedicated folder
    """
    # Configure story parameters first
    configure_story(theme, num_chapters, words_per_chapter)
    
    # Create story folder and set it as environment variable
    story_folder = create_story_folder(story_config.theme)
    os.environ['CURRENT_STORY_FOLDER'] = story_folder
    
    # Create agents and tasks with updated configuration
    crew_config = create_agents_and_tasks()
    
    crew = Crew(
        agents=crew_config['agents'],
        tasks=crew_config['tasks'],
        verbose=True,
        process=Process.sequential
    )
    
    result = crew.kickoff()
    
    # Clean up environment variable
    os.environ.pop('CURRENT_STORY_FOLDER', None)
    
    return result

# Example usage in main
if __name__ == "__main__":
    # Configure PDF style
    story_config.pdf_style.update_colors(
        primary='#2c3e50',    # Dark blue
        secondary='#34495e',   # Medium blue
        accent='#e74c3c',      # Red accent
        background='#ffffff',  # White
        text='#2c3e50'        # Dark blue for text
    )

    story_config.pdf_style.update_fonts(
        main='Arial',
        title='Arial',
        heading='Arial',
        body='Arial'
    )

    story_config.pdf_style.update_sizes(
        title='28pt',
        chapter='22pt',
        body='12pt',
        spacing='1.6'
    )

    # Generate story
    result = generate_story(
        theme="ADN de dragón",
        num_chapters=2,
        words_per_chapter=150
    )
    print(f"Tema después de configurar: {story_config.theme}")
    print(result)

