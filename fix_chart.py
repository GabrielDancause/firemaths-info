with open('public/stock-return-calculator.html', 'r') as f:
    content = f.read()

# I noticed the JS for drawing chart was not complete in generate_html.py
# actually, it looks like it did not handle the end correctly.

import re
match = re.search(r'function drawChart\(labels, data\) \{.*\}\s*// Initial calculate on load', content, flags=re.DOTALL)
if match:
    pass
