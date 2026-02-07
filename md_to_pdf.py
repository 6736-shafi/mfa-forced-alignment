#!/usr/bin/env python3
"""
Convert REPORT.md to a professional-looking PDF using markdown and weasyprint.
"""

import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

# Read the markdown file
with open('REPORT.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

# Convert markdown to HTML with extensions for tables, code highlighting, etc.
md = markdown.Markdown(extensions=[
    'tables',
    'fenced_code',
    'codehilite',
    'toc',
    'meta',
    'attr_list',
    'md_in_html',
])
html_content = md.convert(md_content)

# Professional CSS styling
css_content = """
@page {
    size: A4;
    margin: 2cm 2.5cm;
    @top-center {
        content: "Montreal Forced Aligner: Implementation and Analysis Report";
        font-size: 9pt;
        color: #666;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    @bottom-center {
        content: "Page " counter(page) " of " counter(pages);
        font-size: 9pt;
        color: #666;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
}

@page :first {
    @top-center { content: none; }
}

body {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #333;
    text-align: justify;
    hyphens: auto;
}

h1 {
    font-size: 24pt;
    color: #1a365d;
    border-bottom: 3px solid #2c5282;
    padding-bottom: 12px;
    margin-top: 0;
    margin-bottom: 24px;
    page-break-after: avoid;
    text-align: center;
}

h2 {
    font-size: 16pt;
    color: #2c5282;
    margin-top: 32px;
    margin-bottom: 16px;
    border-bottom: 1.5px solid #4299e1;
    padding-bottom: 8px;
    page-break-after: avoid;
}

h3 {
    font-size: 13pt;
    color: #2d3748;
    margin-top: 24px;
    margin-bottom: 12px;
    page-break-after: avoid;
}

h4 {
    font-size: 11pt;
    color: #4a5568;
    margin-top: 20px;
    margin-bottom: 10px;
    font-weight: 600;
    page-break-after: avoid;
}

p {
    margin-bottom: 12px;
    orphans: 3;
    widows: 3;
}

strong {
    color: #1a365d;
}

em {
    font-style: italic;
    color: #4a5568;
}

/* Code blocks */
pre {
    background-color: #f7fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 16px;
    font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
    font-size: 9pt;
    line-height: 1.5;
    overflow-x: auto;
    page-break-inside: avoid;
    margin: 16px 0;
}

code {
    font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
    font-size: 9pt;
    background-color: #edf2f7;
    padding: 2px 6px;
    border-radius: 3px;
    color: #c53030;
}

pre code {
    background: none;
    padding: 0;
    color: inherit;
}

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    font-size: 10pt;
    page-break-inside: avoid;
}

thead {
    background-color: #2c5282;
    color: white;
}

th {
    padding: 12px 10px;
    text-align: left;
    font-weight: 600;
    border: 1px solid #2c5282;
}

td {
    padding: 10px;
    border: 1px solid #e2e8f0;
}

tbody tr:nth-child(even) {
    background-color: #f7fafc;
}

tbody tr:hover {
    background-color: #edf2f7;
}

/* Lists */
ul, ol {
    margin: 12px 0;
    padding-left: 24px;
}

li {
    margin-bottom: 6px;
}

/* Blockquotes */
blockquote {
    border-left: 4px solid #4299e1;
    padding-left: 16px;
    margin: 16px 0;
    color: #4a5568;
    font-style: italic;
    background-color: #ebf8ff;
    padding: 12px 16px;
    border-radius: 0 6px 6px 0;
}

/* Horizontal rule */
hr {
    border: none;
    border-top: 2px solid #e2e8f0;
    margin: 32px 0;
}

/* Links */
a {
    color: #2c5282;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

/* Cover page styling */
.cover-section {
    text-align: center;
    margin-top: 100px;
}

/* Executive summary box */
h2:first-of-type + p,
h2 + p:first-of-type {
    background-color: #ebf8ff;
    padding: 16px;
    border-radius: 6px;
    border-left: 4px solid #4299e1;
}

/* Key findings highlight */
strong:first-of-type {
    font-size: 11pt;
}

/* ASCII diagram boxes */
pre:has(code.language-) {
    font-size: 8pt;
}

/* Pipeline diagram styling */
pre {
    white-space: pre-wrap;
    word-wrap: break-word;
}

/* Appendix styling */
h2:contains(Appendix) {
    color: #4a5568;
    font-size: 14pt;
}

/* Print-specific */
@media print {
    body {
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }
    
    h2 {
        page-break-before: auto;
    }
    
    table, pre, blockquote {
        page-break-inside: avoid;
    }
}

/* Footer author info */
p:last-of-type {
    font-style: italic;
    color: #718096;
}
"""

# Full HTML document
full_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MFA Forced Alignment Report</title>
</head>
<body>
    {html_content}
</body>
</html>
"""

# Generate PDF
font_config = FontConfiguration()
html = HTML(string=full_html)
css = CSS(string=css_content, font_config=font_config)

print("Converting REPORT.md to PDF...")
html.write_pdf('REPORT.pdf', stylesheets=[css], font_config=font_config)
print("✅ Successfully created REPORT.pdf")
