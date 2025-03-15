"""
Token counting utilities for different LLM providers.
"""
import re
import regex

# Try to import tiktoken, but use fallback if not available
try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False


def count_tokens_anthropic(text):
    """
    Count tokens for Anthropic's Claude using an approximation.

    Args:
        text (str): The text to count tokens for

    Returns:
        int: The approximate token count
    """
    if TIKTOKEN_AVAILABLE:
        try:
            # Claude uses a similar tokenizer to GPT-4
            encoding = tiktoken.get_encoding("cl100k_base")
            return len(encoding.encode(text))
        except Exception:
            # Fall back to approximation if encoding fails
            pass

    # Fallback approximation method
    return count_tokens_fallback(text)


def count_tokens_openai(text, model="gpt-4"):
    """
    Count tokens for OpenAI's GPT models.

    Args:
        text (str): The text to count tokens for
        model (str): The OpenAI model name

    Returns:
        int: The token count
    """
    if TIKTOKEN_AVAILABLE:
        try:
            if model.startswith("gpt-4"):
                encoding = tiktoken.get_encoding("cl100k_base")
            elif model.startswith("gpt-3.5-turbo"):
                encoding = tiktoken.get_encoding("cl100k_base")
            else:
                encoding = tiktoken.get_encoding("p50k_base")

            return len(encoding.encode(text))
        except Exception:
            # Fall back to approximation if encoding fails
            pass

    # Fallback approximation method
    return count_tokens_fallback(text)


def count_tokens_fallback(text):
    """
    Fallback method for token counting using regex approximation.

    Args:
        text (str): The text to count tokens for

    Returns:
        int: The approximate token count
    """
    # Approach based on GPT tokenization patterns
    # This is a simplification and will not match exactly

    # Split on whitespace and punctuation
    words = regex.findall(r'\p{L}+|\p{N}+|\p{P}+|\s+', text)

    # Add a rough adjustment for tokenization patterns:
    # - Short common words tend to be single tokens
    # - Longer words get split into multiple tokens
    # - Numbers and punctuation might be tokens themselves
    token_count = 0
    for word in words:
        if len(word) <= 2:
            token_count += 1  # Short words/chars likely a single token
        else:
            # Approximate longer words based on length
            # This approximation assumes about 4 chars per token on average
            token_count += max(1, round(len(word) / 4))

    return token_count


def count_tokens(text, provider="Claude (Anthropic)"):
    """
    Count tokens based on the LLM provider.

    Args:
        text (str): The text to count tokens for
        provider (str): The LLM provider name

    Returns:
        int: The approximate token count
    """
    if "Claude" in provider:
        return count_tokens_anthropic(text)
    elif "GPT" in provider:
        return count_tokens_openai(text)
    else:
        # Default to OpenAI's tokenizer for other providers
        return count_tokens_openai(text)


def get_context_with_token_limit(text, selection_start, selection_end, token_limit, provider="Claude (Anthropic)"):
    """
    Get text with the given selection and surrounding context up to the token limit.

    Args:
        text (str): The full text
        selection_start (int): The start position of the selection
        selection_end (int): The end position of the selection
        token_limit (int): The maximum number of tokens to include
        provider (str): The LLM provider name

    Returns:
        str: The text with the selection and surrounding context
    """
    # Get the selected text
    selected_text = text[selection_start:selection_end]
    selected_tokens = count_tokens(selected_text, provider)

    # If the selection already exceeds the token limit, truncate it
    if selected_tokens > token_limit:
        # Simple character-based truncation that preserves about 'token_limit' tokens
        # This is an approximation without tiktoken
        chars_to_keep = token_limit * 4  # Rough estimate of 4 chars per token
        if chars_to_keep < len(selected_text):
            # Try to break at a word boundary
            truncated_text = selected_text[:chars_to_keep]
            last_space = truncated_text.rfind(' ')
            if last_space > chars_to_keep // 2:  # Only if it's not cutting off too much
                truncated_text = truncated_text[:last_space]
            return truncated_text
        return selected_text

    # Calculate how many tokens we can add before/after
    tokens_remaining = token_limit - selected_tokens

    # For large texts, add context before and after
    if len(text) > 50000:  # ~20 pages
        # Add context before and after the selection
        before_text = text[:selection_start]
        after_text = text[selection_end:]

        # Calculate tokens for before and after
        before_tokens = count_tokens(before_text, provider)
        after_tokens = count_tokens(after_text, provider)

        # If we can include all the context, return the full text
        if before_tokens + selected_tokens + after_tokens <= token_limit:
            return text

        # Otherwise, calculate how much context to include before and after
        tokens_for_context = tokens_remaining
        before_ratio = 0.5  # Default to 50% before, 50% after

        # Adjust the ratio if we have more text on one side
        if before_tokens < after_tokens and before_tokens < tokens_for_context * before_ratio:
            before_ratio = before_tokens / tokens_for_context
        elif after_tokens < before_tokens and after_tokens < tokens_for_context * (1 - before_ratio):
            before_ratio = 1 - (after_tokens / tokens_for_context)

        # Calculate tokens to include before and after
        tokens_before = int(tokens_for_context * before_ratio)
        tokens_after = tokens_for_context - tokens_before

        # Get the actual text to include - simplified without tiktoken
        if tokens_before > 0:
            # Rough approximation: 4 chars per token
            chars_before = tokens_before * 4
            if len(before_text) > chars_before:
                # Try to break at paragraph or sentence boundary for more natural context
                truncated_before = before_text[-chars_before:]
                paragraph_break = truncated_before.find('\n\n')
                if paragraph_break > 0 and paragraph_break > chars_before // 2:
                    before_text = before_text[-(chars_before -
                                                paragraph_break):]
                else:
                    sentence_break = re.search(r'[.!?]\s+', truncated_before)
                    if sentence_break and sentence_break.start() > chars_before // 3:
                        before_text = before_text[-(chars_before -
                                                    sentence_break.start() - 1):]
                    else:
                        before_text = before_text[-chars_before:]
            # else keep all before_text
        else:
            before_text = ""

        if tokens_after > 0:
            # Rough approximation: 4 chars per token
            chars_after = tokens_after * 4
            if len(after_text) > chars_after:
                truncated_after = after_text[:chars_after]
                paragraph_break = truncated_after.rfind('\n\n')
                if paragraph_break > 0 and paragraph_break > chars_after // 2:
                    after_text = after_text[:paragraph_break]
                else:
                    sentence_break = re.search(r'[.!?]\s+', truncated_after)
                    if sentence_break and sentence_break.start() > chars_after // 3:
                        after_text = after_text[:sentence_break.start() + 1]
                    else:
                        after_text = after_text[:chars_after]
            # else keep all after_text
        else:
            after_text = ""

        return before_text + selected_text + after_text

    # For smaller texts, just return as much as possible
    return text[:token_limit * 4]  # Rough approximation
