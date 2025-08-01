import os
from jinja2 import Template, Environment, FileSystemLoader
from jinja2.defaults import (
    BLOCK_START_STRING,
    BLOCK_END_STRING,
)
from progressbar import ProgressBar, ProgressBarStyle


INPUT_FOLDER = 'templates'
OUTPUT_FOLDER = 'dist'

HTML_COMMENT_START = '<!-- '
HTML_COMMENT_END = ' -->'

# set folder
fsl = FileSystemLoader('templates')

# settings for the output
env = Environment(
    loader=fsl,
    block_start_string=HTML_COMMENT_START + BLOCK_START_STRING,
    block_end_string=BLOCK_END_STRING + HTML_COMMENT_END,
    trim_blocks=True,
    lstrip_blocks=True,
    keep_trailing_newline=True,
    autoescape=False,  # Disable autoescaping for markdown
)

# load the template
template = env.get_template('1.md')

# define render data
data = {
    'h1': 'Template 1',
    'h2_1': 'Skills',
    'pbn': lambda lang, value: ProgressBar(value=value, title=lang, width=200, show_text=False, _title_auto_fill_length=11).generate_url(),
    'pb': lambda value: ProgressBar(value=value, width=200, show_text=False).generate_url(),
    'image': lambda path: f'<img src="{path.replace("<", "").replace(">", "")}" alt="" style="vertical-align: middle; width: 40px; height: 40px;">',
}

# render the template with context
output = template.render(data)

# write the output to a file
print(template.name)
path = os.path.join(OUTPUT_FOLDER, template.name)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
with open(path, 'w', encoding=fsl.encoding) as f:
    f.write(output)
print(
    f"Template rendered and output written to '{path}'.")
