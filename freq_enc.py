import os
import json
from typing import List, Dict, Tuple
from collections import Counter

def freq_enc(text: str) -> str:
    """
    Calculates the frequency-based rank encoding for a single string of 
    space-separated tokens (e.g., "150 273 14 233").

    1. Splits the string into a list of tokens (the numbers).
    2. Ranks the tokens based on their total frequency (most frequent = rank 0).
    3. Maps the original sequence of tokens to their rank IDs.
    """
    tokens = text.split()
    if not tokens:
        return ""

    counts = Counter(tokens)
    
    first_occurrence_order: Dict[str, int] = {
        token: i for i, token in enumerate(tokens) 
        if token not in tokens[:i]
    }

    char_rank_data: List[Tuple[int, int, str]] = []
    for token, freq in counts.items():
        char_rank_data.append((-freq, first_occurrence_order[token], token))
    
    char_rank_data.sort() 
    char_to_rank_id: Dict[str, int] = {}
    for rank_id, (_, _, token) in enumerate(char_rank_data):
        char_to_rank_id[token] = rank_id
    
    encoded_list = [str(char_to_rank_id[token]) for token in tokens]
    return " ".join(encoded_list)


def fairseq_data(input_data_dir: str, train_output_dir: str, test_output_dir: str):
    """
    Reads JSON files, sorts them, and writes the aggregated, space-separated 
    .src/.tgt and .freq files.
    """
    
    os.makedirs(train_output_dir, exist_ok=True)
    os.makedirs(test_output_dir, exist_ok=True)
    
    train_files: List[str] = []
    test_files: List[str] = []
    
    for filename in os.listdir(input_data_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(input_data_dir, filename)
            
            if filename.startswith('test-cipher-'):
                test_files.append(file_path)
            else:
                train_files.append(file_path)

    if not train_files and not test_files:
        print("Error: No JSON files found in the input directory.")
        return

    print(f"Training ciphers identified: {len(train_files)}")
    print(f"Testing ciphers identified: {len(test_files)}")

    write_aggregated_files(train_files, train_output_dir, 'data')
    write_aggregated_files(test_files, test_output_dir, 'data')

    print("\nData preparation complete. Output Structure:")
    print(f"  Training Files: {os.path.join(train_output_dir, 'data.src')}, {os.path.join(train_output_dir, 'data.tgt')} and {os.path.join(train_output_dir, 'data.freq')}")
    print(f"  Testing Files: {os.path.join(test_output_dir, 'data.src')}, {os.path.join(test_output_dir, 'data.tgt')} and {os.path.join(test_output_dir, 'data.freq')}")


def write_aggregated_files(file_list: List[str], output_dir: str, prefix: str):
    """
    Helper function: Writes ciphertexts, plaintexts, and frequency encodings 
    to aggregated .src, .tgt, and .freq files.
    """
    
    cipher_file_path = os.path.join(output_dir, f"{prefix}.src")
    plaintext_file_path = os.path.join(output_dir, f"{prefix}.tgt")

    with open(cipher_file_path, 'w', encoding='utf-8') as f_cipher, \
         open(plaintext_file_path, 'w', encoding='utf-8') as f_plain:
        
        for file_path in file_list:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                ciphertext = data['ciphertext']
                plaintext = data['plaintext']
                
                freq_encoding = freq_enc(ciphertext)
                f_cipher.write(freq_encoding + '\n')
                
                spaced_plain = " ".join(list(plaintext))
                f_plain.write(spaced_plain + '\n')
                
            except json.JSONDecodeError:
                print(f"Warning: Skipping malformed JSON file: {file_path}")
            except KeyError:
                print(f"Warning: Skipping file missing 'ciphertext' or 'plaintext' key: {file_path}")