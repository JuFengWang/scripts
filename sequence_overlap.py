import sys
import argparse

def read_fasta(filename):
    """Read a FASTA file and return a dictionary of sequence names and sequences."""
    sequences = {}
    with open(filename, 'r') as file:
        sequence_name = None
        for line in file:
            if line.startswith(">"):
                sequence_name = line.strip()
                sequences[sequence_name] = ""
            else:
                sequences[sequence_name] += line.strip()
    return sequences

def get_repeat_length(sequence, n):
    """Return the length of the repeat at both ends of the sequence, at least n."""
    for i in range(len(sequence) // 2, n - 1, -1):
        if sequence[:i] == sequence[-i:]:
            return i
    return 0

def write_fasta(sequences, filename):
    """Write sequences to a FASTA file."""
    with open(filename, 'w') as file:
        for name, seq in sequences.items():
            file.write(f"{name}\n{seq}\n")

def main(fasta_file, n, prefix):
    sequences = read_fasta(fasta_file)
    circular_sequences = {}
    uncircular_sequences = {}

    for name, seq in sequences.items():
        repeat_length = get_repeat_length(seq, n)
        if repeat_length >= n:
            circular_sequences[f"{name}_{repeat_length}"] = seq
        else:
            uncircular_sequences[name] = seq

    write_fasta(circular_sequences, f"{prefix}.circular.fa")
    write_fasta(uncircular_sequences, f"{prefix}.uncircular.fa")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter FASTA sequences based on terminal repeats.")
    parser.add_argument("-fa", "--fasta", required=True, help="Input FASTA file")
    parser.add_argument("-n", type=int, required=True, help="Minimum repeat length")
    parser.add_argument("-p", "--prefix", required=True, help="Prefix for output files")

    args = parser.parse_args()
    main(args.fasta, args.n, args.prefix)
