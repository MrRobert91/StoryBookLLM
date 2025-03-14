# StoryBookLLM 📚✨

A powerful AI-powered children's storybook generator that creates illustrated stories using Large Language Models and DALL-E image generation.

## 🌟 Features

- **AI-Driven Story Creation**: Automatically generates complete children's stories with 5 chapters
- **Custom Illustrations**: Creates unique illustrations for each chapter using DALL-E 3
- **Professional PDF Output**: Converts stories into beautifully formatted PDF books
- **Theme Customization**: Generate stories based on specific themes or topics
- **Intelligent Agents**: Uses specialized AI agents for different aspects of story creation

## 🛠️ Technical Architecture

The system uses multiple AI agents working in concert:

1. **Story Outliner**: Creates the story structure and character descriptions
2. **Story Writer**: Develops full narrative content for each chapter
3. **Image Generator**: Creates custom illustrations using DALL-E 3
4. **Content Formatter**: Organizes content in Markdown format
5. **PDF Converter**: Produces the final PDF document

## 📋 Requirements

```bash
pip install -r requirements.txt
```

Required Python packages:
- markdown2
- beautifulsoup4
- xhtml2pdf
- reportlab
- openai
- [other dependencies...]

## 🚀 Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/StoryBookLLM.git
cd StoryBookLLM
```

2. Set up your environment variables:
```bash
# Create a .env file with your OpenAI API key
OPENAI_API_KEY=your_api_key_here
```

3. Generate a story:
```python
python storyGenerator.py --theme "Space Adventure"
```

## 📖 Usage

```python
# Example of generating a story
from storyGenerator import generate_story

# Generate a story about dragons
story = generate_story(theme="Dragons")
```

## 🔧 Configuration

The system can be configured through several parameters:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `theme` | Story theme | "Adventure" |
| `chapters` | Number of chapters | 5 |
| `words_per_chapter` | Words per chapter | 100 |

## 📂 Project Structure

```
StoryBookLLM/
├── storyGenerator.py    # Main story generation logic
├── agents/             # AI agent definitions
├── templates/          # PDF and story templates
├── output/            # Generated stories and images
└── utils/             # Helper functions
```

## 🎨 Customization

You can customize various aspects of the story generation:

- PDF styling through CSS
- Story structure and length
- Image generation parameters
- Output format preferences

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT and DALL-E APIs
- The open-source community for various tools and libraries

## 📞 Contact

For questions and support, please open an issue in the GitHub repository.

---

Made with ❤️ by [Your Name]
