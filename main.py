from freq_enc import fairseq_data


def main():
    fairseq_data('ciphers_copy', 'train', 'test')


if __name__ == "__main__":
    main()
