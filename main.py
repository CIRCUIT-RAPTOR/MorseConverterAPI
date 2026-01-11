from fastapi import FastAPI, HTTPException
from typing import Dict
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="Morse Code Converter API")

base_path = os.path.dirname(os.path.abspath(__file__))

# International Morse Code Mapping
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', '0': '-----', ' ': '/'
}

# Reverse mapping for decoding
REVERSE_DICT = {value: key for key, value in MORSE_CODE_DICT.items()}

def validate_text(text: str):
    unsupported = [char for char in text.upper() if char not in MORSE_CODE_DICT]
    if unsupported:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported characters found: {list(set(unsupported))}"
        )

def validate_morse(morse: str):
    # Valid tokens: '.', '-', '/', and space
    parts = morse.split()
    unsupported = [p for p in parts if p not in REVERSE_DICT and p != '/']
    if unsupported:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid Morse sequences found: {list(set(unsupported))}"
        )

@app.get("/encode")
async def encode_text(text: str):
    """Converts Plain Text to Morse Code."""
    text = text.upper().strip()
    validate_text(text)
    
    encoded = []
    for char in text:
        encoded.append(MORSE_CODE_DICT[char])
    
    return {"input": text, "output": " ".join(encoded).replace(" / ", " / ")}

@app.get("/decode")
async def decode_morse(morse: str):
    """Converts Morse Code to Plain Text."""
    morse = morse.strip()
    validate_morse(morse)
    
    # Split by space to get individual letters/symbols
    words = morse.split(" / ")
    decoded_message = []
    
    for word in words:
        decoded_word = "".join([REVERSE_DICT[letter] for letter in word.split()])
        decoded_message.append(decoded_word)
        
    return {"input": morse, "output": " ".join(decoded_message)}

@app.get("/")
async def read_index():
    # Construct an absolute path to the index.html file
    index_path = os.path.join(base_path, "static", "index.html")
    
    if not os.path.exists(index_path):
        return {"error": f"File not found at {index_path}. Please ensure the 'static' folder exists."}
        

    return FileResponse(index_path)
