import os, subprocess
from bioutils.run_external import path_check

class Prodigal(object):
    """Runs Prodigal"""
    def __init__(self, user_path = None, id_type = 'meta', verbose = True):
        """Class for running Prodigal for CDS prediction

        Args:
            user_path (str, optional): Path for calling Prodigal. Defaults to None, which is the base Path.
            id_type (str, optional): Which mode Prodigal runs in, either 'single' (isolate genome) or 'meta'. Defaults to 'meta'.
            verbose (bool, optional): If true, prints Prodigal output to console. Defaults to True.
        """
        self.user_path = user_path
        self.verbose = verbose
        path_check('prodigal', self.user_path)
        if id_type == 'meta':
            self.id_type = 'meta'
        elif id_type == 'normal':
            self.id_type = 'normal'
        
    def run_prodigal(self, input_fasta, output_gbk, output_aa):
        """Runs Prodigal, generating GBK and amino acid FASTA

        Args:
            input_fasta (str): Path to input nucleotide FASTA
            output_gbk (str): Path to place output GBK
            output_aa (str): Path to place output amino acid FASTA
        """
        if self.verbose:
            prodigal_cmd = ['prodigal', '-i', input_fasta, '-o', output_gbk, '-a', output_aa, '-p', self.id_type]
        else:
            prodigal_cmd = ['prodigal', '-i', input_fasta, '-o', output_gbk, '-a', output_aa, '-p', self.id_type, '-q']
        if not os.path.exists(output_gbk) and not os.path.exists(output_aa):
            subprocess.run(prodigal_cmd)    
