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



# Carga las variables desde el archivo .env
load_dotenv()

# Ahora puedes acceder a las variables de entorno
LANGCHAIN_TRACING_V2 = os.getenv('LANGCHAIN_TRACING_V2')
LANGCHAIN_API_KEY = os.getenv('LANGCHAIN_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')


#Variables para crear la historia de forma dinamica
theme = "Quantum entanglement" #Robots, Animals SciFi etc



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


@tool
def generateimage(chapter_content_and_character_details: str | dict) -> str:
    """
    Generates an image for a given chapter number, chapter content, detailed location details and character details.
    Using the OpenAI image generation API,
    saves it in the current folder, and returns the image path.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Handle both string and dictionary input
    content = (chapter_content_and_character_details['description'] 
              if isinstance(chapter_content_and_character_details, dict) 
              else chapter_content_and_character_details)

    print("----chapter_content_and_character_details: ----")
    print(type(content))
    print(content)

    dalle_prompt = f"Image is about: {content}. Style: Illustration. Create an illustration incorporating a vivid palette with an emphasis on shades of azure and emerald, augmented by splashes of gold for contrast and visual interest. The style should evoke the intricate detail and whimsy of early 20th-century storybook illustrations, blending realism with fantastical elements to create a sense of wonder and enchantment. The composition should be rich in texture, with a soft, luminous lighting that enhances the magical atmosphere. Attention to the interplay of light and shadow will add depth and dimensionality, inviting the viewer to delve into the scene. DON'T include ANY text in this image. DON'T include colour palettes in this image."

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
    words = content.split()[:5] 
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

@tool
def convermarkdowntopdf(markdownfile_name: str) -> str:
    """
    Converts a Markdown file to a PDF document using xhtml2pdf.
    """
    import markdown2
    from xhtml2pdf import pisa
    from bs4 import BeautifulSoup
    import base64
    from datetime import datetime
    
    date_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = os.path.splitext(markdownfile_name)[0] + theme + "-" + date_now + '.pdf'
    
    # Leer el contenido del Markdown
    with open(markdownfile_name, 'r', encoding='utf-8') as md_file:
        markdown_content = md_file.read()
    
    # Convertir Markdown a HTML
    html_content = markdown2.markdown(
        markdown_content,
        extras=['fenced-code-blocks', 'tables', 'header-ids', 'images']
    )
    
    # Procesar imágenes
    soup = BeautifulSoup(html_content, 'html.parser')
    for img in soup.find_all('img'):
        src = img.get('src')
        if src and not src.startswith(('http://', 'https://', 'data:')):
            absolute_path = os.path.abspath(os.path.join(os.path.dirname(markdownfile_name), src))
            if os.path.exists(absolute_path):
                with open(absolute_path, 'rb') as img_file:
                    img_data = base64.b64encode(img_file.read()).decode('utf-8')
                    img['src'] = f'data:image/png;base64,{img_data}'
    
    html_content = str(soup)
    
    # CSS para el diseño
    css = '''
        @page {
            size: A4;
            margin: 2cm;
        }
        body {
            font-family: Helvetica, Arial, sans-serif;
            font-size: 12pt;
            line-height: 1.6;
        }
        h1 {
            font-size: 24pt;
            color: #2c3e50;
            text-align: center;
            margin-bottom: 20pt;
        }
        h2 {
            font-size: 18pt;
            color: #34495e;
            margin-top: 16pt;
        }
        img {
            max-width: 90%;
            margin: 20pt auto;
            display: block;
        }
        p {
            text-align: justify;
            margin-bottom: 10pt;
        }
    '''
    
    # HTML completo con CSS
    html = f'''
        <html>
        <head>
            <meta charset="UTF-8">
            <style>{css}</style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
    '''
    
    # Convertir HTML a PDF
    with open(output_file, "wb") as pdf_file:
        pisa_status = pisa.CreatePDF(
            html,
            dest=pdf_file,
            encoding='utf-8'
        )
    
    if pisa_status.err:
        print('Error al generar el PDF')
        return ""
    
    print(f"PDF generado con éxito: {output_file}")
    return output_file

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


@tool
def newconvermarkdowntopdf(markdownfile_name: str) -> str:
    """
    Converts a Markdown file to a PDF document using the MarkdownPdf python library.

    Args:
        markdownfile_name (str): Path to the input Markdown file.

    Returns:
        str: Path to the generated PDF file.
    """

    date_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Formato: YYYY-MM-DD_HH-MM-SS

    output_file = os.path.splitext(markdownfile_name)[0] + theme + "-" + date_now + '.pdf'

    with open(markdownfile_name, 'r', encoding='utf-8') as md_file:
            markdown_content = md_file.read()

    #--------------------
    pdf = MarkdownPdf(toc_level=2)
    pdf.meta["title"] = theme
    pdf.add_section(Section(markdown_content, toc=False))
    pdf.save(output_file)


        
    return output_file



story_outliner = Agent(
  role='Story Outliner',
  goal=f"Develop an outline for a children\'s storybook about {theme}, including chapter titles and characters for 5 chapters.",
  backstory="An imaginative creator who lays the foundation of captivating stories for children.",
  verbose=True,
  llm=llm,
  allow_delegation=False
)

story_writer = Agent(
  role='Story Writer',
  goal='Write the full content of the story for all 5 chapters, each chapter 100 words, weaving together the narratives and characters outlined.',
  backstory="A talented storyteller who brings to life the world and characters outlined, crafting engaging and imaginative tales for children.",
  verbose=True,
  llm=llm,
  allow_delegation=False
)

image_generator = Agent(
  role='Image Generator',
  goal='Generate one image per chapter content provided by the story outliner. Start with Chapter number, chapter content, character details, detailed location information and detailed items in the location where the activity happens. Generate totally 5 images one by one. Final output should contain all the 5 images in json format.',
  backstory="A creative AI specialized in visual storytelling, bringing each chapter to life through imaginative imagery.",
  verbose=True,
  llm=llm,
  tools=[generateimage],
  allow_delegation=False
)

content_formatter = Agent(
    role='Content Formatter',
    goal='Format the written story content in markdown, including images at the beginning of each chapter.',
    backstory='A meticulous formatter who enhances the readability and presentation of the storybook.',
    verbose=True,
    llm=llm,
    tools=[file_read_tool],
    allow_delegation=False
)

markdown_to_pdf_creator = Agent(
    role='PDF Converter',
    goal='Convert the Markdown file to a PDF document. story.md is the markdown file name.',
    backstory='An efficient converter that transforms Markdown files into professionally formatted PDF documents.',
    verbose=True,
    llm=llm,
    tools=[convermarkdowntopdf],  # newconvermarkdowntopdf
    allow_delegation=False
)


# Create tasks for the agents
task_outline = Task(
    description=f"Create an outline for the children\'s storybook about {theme}, detailing chapter titles and character descriptions for 5 chapters.",
    agent=story_outliner,
    expected_output='A structured outline document containing 5 chapter titles, with detailed character descriptions and the main plot points for each chapter.'
)

task_write = Task(
    description='Using the outline provided, write the full story content for all chapters, ensuring a cohesive and engaging narrative for children. Each Chapter 100 words. Include Title of the story at the top.',
    agent=story_writer,
    expected_output=f"A complete manuscript of the children\'s storybook about {theme} with 5 chapters. Each chapter should contain approximately 100 words, following the provided outline and integrating the characters and plot points into a cohesive narrative."
)

task_image_generate = Task(
    description=f"Generate 5 images that captures the essence of the children\'s storybook about {theme}, aligning with the themes, characters, and narrative outlined for the chapters. Do it one by one.",
    agent=image_generator,
    expected_output='A digital image file that visually represents the overarching theme of the children\'s storybook, incorporating elements from the characters and plot as described in the outline. The image should be suitable for inclusion in the storybook as an illustration.',
)

task_format_content = Task(
    description='Format the story content in markdown, including an image at the beginning of each chapter.',
    agent=content_formatter,
    expected_output='The entire storybook content formatted in markdown, with each chapter title followed by the corresponding image and the chapter content. remove the  ```markdown sintax from the output',
    context=[task_write, task_image_generate],
    output_file="story.md"
)

task_markdown_to_pdf = Task(
    description='Convert a Markdown file to a PDF document, ensuring the preservation of formatting, structure, and embedded images using the mdpdf library.',
    agent=markdown_to_pdf_creator,
    expected_output='A PDF file generated from the Markdown input, accurately reflecting the content with proper formatting. The PDF should be ready for sharing or printing.'
)

crew = Crew(
  agents=[story_outliner, story_writer, image_generator, content_formatter, markdown_to_pdf_creator],
  tasks=[task_outline, task_write, task_image_generate, task_format_content, task_markdown_to_pdf],
  verbose=True,
  process=Process.sequential
)

result = crew.kickoff()

print(result)

