import hashlib
import os
import time
import json

# Initialize a chain of custody log
chain_of_custody = []

# Function to compute the SHA-256 hash of a file
def compute_hash(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        return None

# Function to simulate forensic imaging (bit-by-bit copy)
def forensic_image(source_path, destination_path):
    try:
        with open(source_path, "rb") as src, open(destination_path, "wb") as dest:
            while chunk := src.read(4096):
                dest.write(chunk)
        return True
    except Exception as e:
        print(f"Error during imaging: {e}")
        return False

# Function to log an event in the chain of custody
def log_chain_of_custody(action, file_path, person):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    event = {
        "timestamp": timestamp,
        "action": action,
        "file": file_path,
        "person": person
    }
    chain_of_custody.append(event)

# Function to display the chain of custody
def display_chain_of_custody():
    print("\nChain of Custody Log:")
    print(json.dumps(chain_of_custody, indent=4))

# Main function
def main():
    print("Welcome to Forensic Imaging System")
    
    # Step 1: Input file for imaging
    source_file = input("Enter the path of the source evidence file: ")
    if not os.path.exists(source_file):
        print("Source file not found!")
        return

    # Step 2: Compute original hash
    original_hash = compute_hash(source_file)
    if not original_hash:
        print("Error: Unable to compute hash of the source file.")
        return
    print(f"Original File Hash (SHA-256): {original_hash}")

    # Log the hash computation
    log_chain_of_custody("Computed original hash", source_file, "Forensic Analyst")

    # Step 3: Create a forensic image
    destination_file = input("Enter the path to save the forensic image: ")
    if forensic_image(source_file, destination_file):
        print("Forensic image created successfully.")
        log_chain_of_custody("Created forensic image", destination_file, "Forensic Analyst")
    else:
        print("Error during forensic imaging!")
        return

    # Step 4: Compute hash of the forensic image
    image_hash = compute_hash(destination_file)
    print(f"Forensic Image Hash (SHA-256): {image_hash}")
    log_chain_of_custody("Computed hash of forensic image", destination_file, "Forensic Analyst")

    # Step 5: Verify integrity
    if original_hash == image_hash:
        print("Verification Passed: The forensic image matches the original evidence.")
        log_chain_of_custody("Verified integrity of forensic image", destination_file, "Forensic Analyst")
    else:
        print("Verification Failed: The forensic image does not match the original evidence.")
        log_chain_of_custody("Verification failed", destination_file, "Forensic Analyst")

    # Display the chain of custody
    display_chain_of_custody()

# Run the program
if __name__ == "__main__":
    main()
