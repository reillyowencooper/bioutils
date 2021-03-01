# Named this run_hmmer even though it's only hmmsearch for potential future uses of hmmpress and hmmbuild
# Biopython has an HMM parser, but it's relatively clunky

import os, subprocess
from bioutils.run_external import path_check

class Hmmer(object):
    """Runs HMMsearch for now, but is generalizable for other HMMER subprograms
    """
    def __init__(self, user_path = None):
        self.user_path = user_path
        path_check('hmmsearch', self.user_path)
        
    def run_hmmsearch(self, output_path, input_file, hmm_db):
        """Runs an HMMsearch on an input FASTA given an HMM database, returning a domain table tabular format

        Args:
            output_path (str): Path to deposit domtblout file
            input_file (str): Path to input FASTA (should be protein format)
            hmm_db (str): Path to HMM database
        """
        hmmsearch_cmd = ['hmmsearch', '--domtblout', output_path, hmm_db, input_file]
        if not os.path.exists(output_path):
            subprocess.run(hmmsearch_cmd)
            

class HmmHit(object):
    """Stores a single line of an HMMsearch domtblout with every element as its own value"""
    def __init__(self, domtblout_line):
        """Expects a list of 23 elements"""
        self.target_name = str(domtblout_line[0])
        self.target_acc = str(domtblout_line[1])
        if self.target_acc == '-':
            self.target_acc = self.target_name # This happens often
        self.target_len = int(domtblout_line[2])
        self.query_name = str(domtblout_line[3])
        self.query_acc = str(domtblout_line[4])
        if self.query_acc == '-':
            self.query_acc = self.query_name
        self.query_len = int(domtblout_line[5])
        self.e_value = float(domtblout_line[6])
        self.bitscore = float(domtblout_line[7])
        self.bias = float(domtblout_line[8])
        self.domain_number = int(domtblout_line[9])
        self.total_domains = int(domtblout_line[10])
        self.conditional_evalue = float(domtblout_line[11])
        self.independent_evalue = float(domtblout_line[12])
        self.domain_bitscore = float(domtblout_line[13])
        self.domain_bias = float(domtblout_line[14])
        self.hmm_from = int(domtblout_line[15])
        self.hmm_to = int(domtblout_line[16])
        self.ali_from = int(domtblout_line[17])
        self.ali_to = int(domtblout_line[18])
        self.env_from = int(domtblout_line[19])
        self.env_to = int(domtblout_line[20])
        self.posterior_probability = float(domtblout_line[21])
        self.description = float(domtblout_line[22])
        self.target_coverage = float(self.ali_to - self.ali_from + 1) / self.target_len
        self.query_coverage = float(self.query_to - self.query_from + 1) / self.query_len
        
                    
class HmmsearchParser(object):
    """Parses HMMsearch domtblout format using HmmHit for each line, putting each line's hits into a list of HmmHits
    """
    def __init__(self, hmmfile):
        """Set with a domtblout file from an HMMsearch"""
        self.hmmfile = hmmfile
        
    def parse_hmmsearch(self):
        hits = []
        with open(self.hmmfile, 'r') as domtbl:
            for line in domtbl:
                if line.startswith('#') or len(line) == 0:
                    continue
                else:
                    line = line.rstrip().split()
                    line = line[0:22] + [' '.join([str(i) for i in line[22:]])]
                    line_parsed = HmmHit(line)
                    hits.append(line_parsed)
        return hits
                    
        