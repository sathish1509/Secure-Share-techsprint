from django import template
import re
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name="highlight_word")
def highlight_word(text, word):
    """
    Highlights all occurrences of a specific word in text with a colored span
    Usage: {{ description|highlight_word:"this" }}
    """
    # If text is None, return empty string
    if not text:
        return ""
    
    # Pattern to match the whole word only (not as part of other words)
    pattern = r'\b' + re.escape(word) + r'\b'
    
    # Replace with HTML span element with primary color and bold text
    replacement = r'<span class="text-primary fw-bold">\g<0></span>'
    
    # Perform the replacement and mark as safe for HTML output
    highlighted_text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return mark_safe(highlighted_text)

@register.filter
def highlight_content_words(text):
    """
    Highlight all important content words in the text.
    Example usage: {{ description|highlight_content_words }}
    """
    if not text:
        return text
    
    # List of important words to highlight
    important_words = [
        'course', 'learn', 'develop', 'skills', 'knowledge', 'understand',
        'practice', 'master', 'this', 'improve', 'create', 'build', 'design',
        'analyze', 'explore', 'discover', 'comprehensive', 'essential', 'fundamental',
        'advanced', 'beginner', 'intermediate', 'expert', 'professional', 'industry'
    ]
    
    result = text
    
    # Highlight each important word
    for word in important_words:
        pattern = r'\b(' + re.escape(word) + r')\b'
        replacement = r'<span class="highlighted-word">\1</span>'
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    
    return mark_safe(result)
