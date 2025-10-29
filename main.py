from freq_enc import fairseq_data, freq_enc


def main():
    fairseq_data('ciphers_copy', 'data')
    """
    infile = open("cipher-30/cipher-30.txt", 'r', encoding='utf-8') 
    outfile = open("cipher-30/cipher-30-enc.txt", 'w', encoding='utf-8')
    for line in infile:
        line = line.strip()
        encoded_line = freq_enc(line)
        outfile.write(encoded_line + "\n")
    """

if __name__ == "__main__":
    main()
