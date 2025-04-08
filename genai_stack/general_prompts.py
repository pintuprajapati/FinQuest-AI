chunking_metadata_prompt_template = """
Generate metadata for the following text chunk.

Text:
\"\"\"{chunk}\"\"\"

Return a short, quirky title (max 6 words), a theme (1 line), and a list of 3-5 relevant tags.
Format your response as JSON with keys: title, theme, tags.

Return JSON in the following format:
{{
  "title": "...",
  "theme": "...",
  "tags": ["...", "..."]
}}
"""