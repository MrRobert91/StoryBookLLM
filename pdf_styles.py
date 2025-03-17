class PDFStyle:
    def __init__(self):
        # Simple color scheme
        self.color_scheme = {
            'primary': '#3368ff',    # Blue - 333333Dark gray for headings
            'secondary': '#666666',   # Medium gray for subheadings
            'accent': '#000000',      # Black for accents
            'background': '#666666',  # grey - White background
            'text': '#333333'        # Dark gray for text
        }
        
        # Basic, widely available fonts
        self.fonts = {
            'main': 'Arial',
            'title': 'Times New Roman',
            'heading': 'Arial',
            'body': 'Arial'
        }
        
        # Conservative sizes
        self.sizes = {
            'title': '24pt',
            'chapter': '18pt',
            'body': '12pt',
            'spacing': '1.5'
        }

    def update_colors(self, primary=None, secondary=None, accent=None, background=None, text=None):
        """
        Update color scheme with specific colors
        Args:
            primary (str): Primary color hex code
            secondary (str): Secondary color hex code
            accent (str): Accent color hex code
            background (str): Background color hex code
            text (str): Text color hex code
        """
        if primary: self.color_scheme['primary'] = primary
        if secondary: self.color_scheme['secondary'] = secondary
        if accent: self.color_scheme['accent'] = accent
        if background: self.color_scheme['background'] = background
        if text: self.color_scheme['text'] = text

    def update_fonts(self, main=None, title=None, heading=None, body=None):
        """
        Update fonts with specific font families
        Args:
            main (str): Main font family
            title (str): Title font family
            heading (str): Heading font family
            body (str): Body font family
        """
        if main: self.fonts['main'] = main
        if title: self.fonts['title'] = title
        if heading: self.fonts['heading'] = heading
        if body: self.fonts['body'] = body

    def update_sizes(self, title=None, chapter=None, body=None, spacing=None):
        """
        Update sizes with specific values
        Args:
            title (str): Title font size (e.g., '28pt')
            chapter (str): Chapter font size (e.g., '22pt')
            body (str): Body font size (e.g., '12pt')
            spacing (str): Line spacing value (e.g., '1.6')
        """
        if title: self.sizes['title'] = title
        if chapter: self.sizes['chapter'] = chapter
        if body: self.sizes['body'] = body
        if spacing: self.sizes['spacing'] = spacing

    def generate_css(self):
        """Generate simple CSS that works reliably with PDF generation"""
        return f"""
            @page {{
                size: A4;
                margin: 2.5cm;
            }}

            body {{
                font-family: {self.fonts['body']}, sans-serif;
                font-size: {self.sizes['body']};
                line-height: {self.sizes['spacing']};
                color: {self.color_scheme['text']};
                background-color: {self.color_scheme['background']};
            }}

            h1 {{
                font-family: {self.fonts['title']}, serif;
                font-size: {self.sizes['title']};
                color: {self.color_scheme['primary']};
                text-align: center;
                margin: 2cm 0 1cm 0;
                padding-bottom: 0.5cm;
            }}

            h2 {{
                font-family: {self.fonts['heading']}, sans-serif;
                font-size: {self.sizes['chapter']};
                color: {self.color_scheme['secondary']};
                page-break-before: always;
                margin-top: 1cm;
            }}

            img {{
                max-width: 80%;
                margin: 1cm auto;
                display: block;
                page-break-inside: avoid;
            }}

            p {{
                text-align: justify;
                margin-bottom: 0.5cm;
            }}
        """