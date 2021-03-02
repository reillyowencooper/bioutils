import os, subprocess
from bioutils.run_external import path_check
from bioutils import utilities

class Mmseqs(object):
    """Runs various Mmseqs modules"""
    def __init__(self, user_path = None, tmp_path = None, mode = 'search', fasta_type = 'nuc'):
        self.user_path = user_path
        self.tmp_path = tmp_path
        if mode == 'createdb':
            self.mode = 'createdb'
        elif mode == 'search':
            self.mode = 'search'
        elif mode == 'taxonomy':
            self.mode = 'taxonomy'
        if fasta_type == 'nuc':
            self.fasta_type = 'nuc'
        elif fasta_type == 'aa':
            self.fasta_type = 'aa'
        path_check('mmseqs', self.user_path)
        
    def create_mmseqs_database(self, input_fasta, output_dir):
        """Creates an MMseqs database from an input fasta"""
        if self.mode == 'createdb':
            fname = utilities.remove_extension(input_fasta)
            createdb_cmd = ['mmseqs', 'createdb', input_fasta, os.path.join(output_dir, fname + '.db')]
            if not os.path.exists(os.path.join(output_dir, fname + '.db')):
                subprocess.run(createdb_cmd)
    
    def search(self, query_db, search_db, output_dir, top_hit = True):
        """Searches input database against a search database and returns a Blast-style OUTFMT6 table"""
        if self.mode == 'search':
            if self.fasta_type == 'nuc':
                search_type = '3'
            else:
                search_type = '1'
            query_name = utilities.remove_extension(query_db)
            search_name = utilities.remove_extension(search_db)
            outdb = os.path.join(output_dir, query_name + '_' + search_name + '.db')
            search_cmd = ['mmseqs', 'search', query_db, search_db, outdb, self.tmp_path, '--search-type', search_type]
            if not os.path.exists(outdb):
                subprocess.run(search_cmd)
            if top_hit:
                topdb = os.path.join(output_dir, query_name + '_' + search_name + '_top.db')
                top_hit_cmd = ['mmseqs', 'filterdb', outdb, topdb, '--extract-lines', '1']
                if not os.path.exists(topdb):
                    subprocess.run(top_hit_cmd)
                    self.convert_alis(query_db, search_db, topdb, output_dir)
            else:
                self.convert_alis(query_db, search_db, outdb)
            
    def convert_alis(self, query_db, search_db, hit_db, output_dir):
        outfmt = os.path.join(output_dir, utilities.remove_extension(hit_db) + '.tab')
        convert_cmd = ['mmseqs', 'convertalis', query_db, search_db, hit_db, outfmt]
        if not os.path.exists(outfmt):
            subprocess.run(convert_cmd)      
    
    def identify_taxonomy(self, query_db, search_db, output_dir):
        if self.mode == 'taxonomy':
            query_name = utilities.remove_extension(query_db)
            search_name = utilities.remove_extension(search_db)
            outdb = os.path.join(output_dir, query_name + '_' + search_name + '.db')
            outtsv = os.path.join(output_dir, query_name + '_' + search_name + '.tsv')
            taxonomy_cmd = ['mmseqs', 'taxonomy', query_db, search_db, outtsv, self.tmp_path, '--tax-lineage', '1']
            tsv_cmd = ['mmseqs', 'createtsv', query_db, outdb, outtsv]
            if not os.path.exists(outtsv):
                if not os.path.exists(outdb):
                    subprocess.run(taxonomy_cmd)
                subprocess.run(tsv_cmd)
            
        
class MmseqsTaxonomyHit(object):
    """Stores a single line of an MMseqs taxonomy search"""
    def __init__(self, taxonomy_tsv_line):
        """Expects a list of 5 elements"""
        self.query_name = str(taxonomy_tsv_line[0])
        self.ncbi_id = int(taxonomy_tsv_line[1])
        self.ncbi_rank = str(taxonomy_tsv_line[2])
        self.ncbi_name = str(taxonomy_tsv_line[3])
        self.complete_lineage = taxonomy_tsv_line[5]


class MmseqsSearchHit(object):
    """Stores a single line of an MMseqs sequence search"""
    def __init__(self, search_tsv_line):
        """Expects a list of 12 elements"""
        self.query_name = str(search_tsv_line[0])
        self.target_name = str(search_tsv_line[1])
        self.sequence_identity = float(search_tsv_line[2])
        self.alignment_len = int(search_tsv_line[3])
        self.num_mismatch = int(search_tsv_line[4])
        self.num_gaps = int(search_tsv_line[5])
        self.query_start = int(search_tsv_line[6])
        self.query_end = int(search_tsv_line[7])
        self.target_start = int(search_tsv_line[8])
        self.target_end = int(search_tsv_line[9])
        self.e_value = float(search_tsv_line[10])
        self.bitscore = float(search_tsv_line[11])
        
  
class MmseqsParser(object):
    """Parses an MMseqs output file in tab format
    
    Uses different parser depending on the type of MMseqs module (right now only taxonomy and search supported)
    """
    def __init__(self, input_file, input_type = 'search'):
        self.input_file = input_file
        if input_type == 'search':
            self.input_type = 'search'
        elif input_type == 'taxonomy':
            self.input_type = 'taxonomy'
            
    def parse_table(self):
        hits = []
        if self.input_type == 'search':
            with open(self.input_file, 'r') as searchfile:
                for line in searchfile:
                    line = line.rstrip().split('\t')
                    line_parsed = MmseqsSearchHit(line)
                    hits.append(line_parsed)
        elif self.input_type == 'taxonomy':
            with open(self.input_file, 'r') as taxfile:
                for line in taxfile:
                    line = line.rstrip().split('\t')
                    line_parsed = MmseqsTaxonomyHit(line)
                    hits.append(line_parsed)
        return hits