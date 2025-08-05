bias_detection_prompt = """
You are a bias detection expert. Analyze this text:

"{input_text}"

Return a JSON with:
- biased_sentences
- bias_types
- summary
"""
