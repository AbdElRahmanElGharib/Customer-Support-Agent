def chunk_text(text, chunk_size=300, overlap=50):
    """
    Splits text into chunks with given size and overlap.
    
    Args:
        text (str): input text
        chunk_size (int): number of tokens/words per chunk
        overlap (int): number of tokens/words to overlap
    
    Returns:
        list[str]: list of text chunks
    """
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap  # move forward with overlap
    return chunks

if __name__ == "__main__":
    sample_text = "This is a sample text to demonstrate the chunking function. " * 20
    chunks = chunk_text(sample_text, chunk_size=10, overlap=2)
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i}: {chunk}")
