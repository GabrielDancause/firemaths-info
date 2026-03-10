import os
import re

directory = 'public'
script_tag = '\n<script src="/nav.js"></script>'

count_before = 0
count_after = 0
modified_files = []

for root, _, files in os.walk(directory):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            count_before += 1

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if script already exists
            if '<script src="/nav.js"></script>' in content:
                print(f"Already injected in {filepath}")
                count_after += 1
                continue

            # Replace <body ...> with <body ...>\n<script src="/nav.js"></script>
            # Use regex to handle body with attributes
            # The regex looks for <body followed by any characters except >, then >,
            # and replaces it with the matched string plus the script tag.
            new_content, num_subs = re.subn(r'(<body[^>]*>)', r'\1' + script_tag, content, count=1, flags=re.IGNORECASE)

            if num_subs > 0:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                modified_files.append(filepath)
                count_after += 1
            else:
                print(f"Warning: No <body> tag found in {filepath}")

print(f"Found {count_before} HTML files.")
print(f"Successfully added script to {count_after} HTML files.")
print(f"Modified {len(modified_files)} files.")
