import os, subprocess
from bioutils.run_external import path_check
from bioutils import utilities

class CheckM(object):
    """Runs CheckM on a set of genomes"""
    def __init__(self, user_path, method = "lineage_wf", domain = None, genome_type = 'fna', threads = 1):
        """Initializes with a path to directory containing genomes in nucleotide or amino acid FASTA format

        Args:
            user_path (str): Path for CheckM install
            method (str): Which CheckM workflow to use (lineage_wf or taxonomy_wf)
            domain (str): If taxonomy_wf is chosen, specifies which taxonomic domain to use (e.g., Bacteria)
            threads (int): Number of threads to use for CheckM
        """
        self.user_path = user_path
        if method == 'lineage_wf':
            self.method = 'lineage_wf'
        elif method == 'taxonomy_wf':
            self.method = 'taxonomy_wf'
        self.domain = domain
        if genome_type == 'fna':
            self.genome_type = 'fna'
        elif genome_type == 'fa':
            self.genome_type = 'fa'
        elif genome_type == 'faa':
            self.genome_type = 'faa'
        self.threads = str(threads)
        path_check('checkm', self.user_path)
            
    def run_checkm_workflow(self, genome_dir, output_dir, output_tsv):
        utilities.create_directory(output_dir)
        if self.method == 'lineage_wf':
            checkm_cmd = ['checkm', self.method, genome_dir, output_dir, '-f', output_tsv, '--tab-table', '-x', self.genome_type, '-t', self.threads]
        elif self.method == 'taxonomy_wf':
            checkm_cmd = ['checkm', self.method, 'domain', self.domain, genome_dir, output_dir, '-f', output_tsv, '--tab-table', '-x', self.genome_type, '-t', threads]
        if self.genome_type == 'faa':
            checkm_cmd.append('-g')
        if not os.path.exists(output_tsv):
            subprocess.run(checkm_cmd)
            

class CheckMHit(object):
    """Stores one line of the CheckM tabular output file"""
    def __init__(self, checkm_tsv_line):
        """"Expects a list of 26 elements"""
        self.bin_id = str(checkm_tsv_line[0])
        self.marker_lineage = str(checkm_tsv_line[1])
        self.num_genomes = int(checkm_tsv_line[2])
        self.num_markers = int(checkm_tsv_line[3])
        self.num_marker_sets = int(checkm_tsv_line[4])
        self.id_0 = int(checkm_tsv_line[5])
        self.id_1 = int(checkm_tsv_line[6])
        self.id_2 = int(checkm_tsv_line[7])
        self.id_3 = int(checkm_tsv_line[8])
        self.id_4 = int(checkm_tsv_line[9])
        self.id_5plus = int(checkm_tsv_line[10])
        self.completeness = float(checkm_tsv_line[11])
        self.contamination = float(checkm_tsv_line[12])
        self.strain_heterogenity = float(checkm_tsv_line[13])
        self.genome_size = int(checkm_tsv_line[14])
        self.num_ambiguous_bases = int(checkm_tsv_line[15])
        self.num_scaffolds = int(checkm_tsv_line[16])
        self.num_contigs = int(checkm_tsv_line[17])
        self.n50_scaffolds = int(checkm_tsv_line[18])
        self.n50_contigs = int(checkm_tsv_line[19])
        self.longest_scaffold = int(checkm_tsv_line[20])
        self.longest_contig = int(checkm_tsv_line[21])
        self.gc = float(checkm_tsv_line[22])
        self.coding_density = float(checkm_tsv_line[23])
        self.translation_table = str(checkm_tsv_line[24])
        self.num_predicted_genes = int(checkm_tsv_line[25])
        

class CheckMParser(object):
    """Parses CheckM tabular output"""
    def __init__(self, input_file):
        self.input_file = input_file
        
    def parse_table(self):
        hits = []
        with open(self.input_file, 'r') as checkmfile:
            for line in checkmfile:
                line = line.rstrip().split('\t')
                line_parsed = CheckMHit(line)
                hits.append(line_parsed)
        return hits