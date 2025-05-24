import os
import PyPDF2
from google.cloud import texttospeech

# Set Google Cloud authentication credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'audiobook-440914-bae6f945de5e.json'

# Initialize Google Cloud Text-to-Speech client
client = texttospeech.TextToSpeechClient()

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

# Function to split text into smaller chunks while respecting the 5000-byte limit
def split_text(text, chunk_size=5000):
    chunks = []
    current_chunk = ""
    
    for word in text.split():
        test_chunk = current_chunk + " " + word if current_chunk else word
        
        if len(test_chunk.encode('utf-8')) > chunk_size:
            chunks.append(current_chunk)
            current_chunk = word  # Start a new chunk with the current word
        else:
            current_chunk = test_chunk

    # Append the last chunk if any text remains
    if current_chunk:
        chunks.append(current_chunk)
        
    return chunks

# Function to convert text to speech using Google Text-to-Speech
def text_to_speech_google(text, gender_choice, outputfile):
    output_file = f"{outputfile}.mp3"  # Use user-specified output file name with .mp3 extension

    # Gender mapping for voice selection
    gender_map = {
        "male": {
            "name": "en-US-Wavenet-D",  # Male voice
            "gender": texttospeech.SsmlVoiceGender.MALE
        },
        "female": {
            "name": "en-US-Wavenet-C",  # Female voice
            "gender": texttospeech.SsmlVoiceGender.FEMALE
        },
        "neutral": {
            "name": "en-US-Wavenet-B",  # Neutral voice
            "gender": texttospeech.SsmlVoiceGender.NEUTRAL
        }
    }

    # Default to "neutral" if an invalid gender is provided
    voice_info = gender_map.get(gender_choice.lower(), gender_map["neutral"])

    # Configure voice parameters
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",  # Change this to your desired language
        name=voice_info["name"],  # Choose the voice based on gender choice
        ssml_gender=voice_info["gender"]
    )

    # Configure audio encoding (MP3 format)
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Split text into smaller chunks to comply with the API's 5000-byte limit
    chunks = split_text(text)
    audio_content = b""

    for chunk in chunks:
        # Prepare synthesis input from the chunk
        synthesis_input = texttospeech.SynthesisInput(text=chunk)

        # Request speech synthesis for each chunk
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # Append the audio content of each chunk to the final audio content
        audio_content += response.audio_content

    # Write the combined audio content to the output file
    with open(output_file, "wb") as out:
        out.write(audio_content)
    
    # Print the result
    print(f"Audio content written to {output_file}")

# Main function to handle PDF-to-speech conversion
def pdf_to_speech():
    # Get the PDF file path, voice gender, and output file name from the user
    pdf_path = input("Give the pdf file to convert (.pdf) format: ")
    text = extract_text_from_pdf(pdf_path)  # Extract text from the PDF
    gender_choice = input("Enter the gender of voice (male/female/neutral): ")
    outputfile = input("Give the output file name: ")
    
    # If text is extracted from the PDF, proceed to convert it to speech
    if text:
        text_to_speech_google(text, gender_choice, outputfile)
    else:
        print("No text extracted from PDF")

# Run the PDF-to-speech conversion
pdf_to_speech()
