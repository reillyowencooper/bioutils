from Bio import SeqIO
from bioutils import utilities
import itertools


def read_fasta(input_fasta):
    """Reads a FASTA file and returns a dict of header: sequence"""
    fasta_dict = {}
    if input_fasta.endswith('.gz'):
        infasta = utilities.unpack_file(input_fasta)
    else:
        infasta = input_fasta
    for seqrecord in SeqIO.parse(input_fasta, "fasta"):
        seqid = str(seqrecord.id)
        sequence = str(seqrecord.seq)
        fasta_dict[seqid] = sequence
    return fasta_dict


def write_fasta(input_dict, output_file):
    """Writes a FASTA given a dict of header: sequence"""
    with open(output_file, 'a+') as outf:
        for header, sequence in input_dict.values():
            outf.write('>' + header + '\n' + sequence + '\n')
            

def check_fasta_type(input_fasta):
    """Reads a FASTA and checks if it's a protein or nucleotide fasta
    
    This is done by subsampling 10 sequences from the input FASTA, then checking if 
    base counts are above 90% sameness to nucleotide/amino acid alphabets
    
    Returns str: 'nucleotide', 'protein', or 'unknown'
    """
    fasta_dict = read_fasta(input_fasta)
    subsample = dict(itertools.islice(fasta_dict.items(), 10))
    nuc_bases = ['A', 'T', 'G', 'C']
    amino_bases = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
    nuc_seqs = 0
    prot_seqs = 0
    for header, sequence in subsample.items():
        seq_len = len(sequence)
        number_nucleotide_bases = 0
        number_amino_bases = 0
        for base in nuc_bases:
            number_nucleotide_bases += sequence.count(base)
        for base in amino_bases:
            number_amino_bases += sequence.count(base)
        proportion_nucleotide = number_nucleotide_bases/seq_len
        proportion_amino = number_amino_bases/seq_len
        if proportion_nucleotide >= 0.9:
            nuc_seqs += 1
        elif proportion_amino >= 0.9:
            prot_seqs += 1
        if nuc_seqs >= 8:
            return "nucleotide"
        elif prot_seqs >= 8:
            return "protein"
        else:
            return "unknown"
    

def subset_fasta(input_fasta, sequence_headers):
    """Subsets a FASTA from an input FASTA using a list of wanted headers"""
    fasta_dict = read_fasta(input_fasta)
    subset_dict = {header: sequence for header, sequence in fasta_dict.items() if header in sequence_headers}
    return subset_dict


def filter_fasta(input_fasta, minimum_len):
    """Subsets FASTA to sequences with length greater than minimum"""
    fasta_dict = read_fasta(input_fasta)
    filtered_dict = {header: sequence for header, sequence in fasta_dict.items() if len(sequence) >= minimum_len}
    return filtered_dict
    

def calculate_n50(input_fasta):
    """Calculates the N50 of an input nucleotide FASTA

    Args:
        input_fasta (str): Path to input FASTA

    Returns:
        int: N50, or the smallest contig/scaffold length of contigs
        containing half or more of total sequence length
    """
    if check_fasta_type(input_fasta) == "nucleotide":
        fasta_dict = read_fasta(input_fasta)
        seq_lengths = []
        for sequence in fasta_dict.values():
            seq_len = len(sequence)
            seq_lengths.append(seq_len)
        halfsum = sum(seq_lengths)/2
        cumulative_len = 0
        sorted_lengths = sorted(seq_lengths, reverse = True)
        for seq_len in sorted_lengths:
            cumulative_len += seq_len
            if cumulative_len >= halfsum:
                return seq_len
    