#!/usr/bin/env python
# Copyright (C) 2010 by the University of Bristol
# Contact: Mark Rogers <Mark.Rogers@bristol.ac.uk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
cscape_query.py: Predict the Oncogenic Potential of Single Nucleotide Variants (SNVs)
"""
import optparse,os,sys,subprocess,time

# CScape databases:
DEFAULT_CODING_DB    = 'cscape_coding.vcf.gz'
DEFAULT_NONCODING_DB = 'cscape_noncoding.vcf.gz'

NUCLEOTIDES = 'ACGT'

# Prediction types
CODING_PRED    = 'coding'
NONCODING_PRED = 'noncoding'

# Confidence thresholds
DEFAULT_THRESH        = 0.5
CODING_HIGH_THRESH    = 0.89
NONCODING_HIGH_THRESH = 0.70

# Confidence ratings
NEUTRAL   = 'Neutral'
LOW_CONF  = 'Low-confidence'
HIGH_CONF = 'High-confidence'
NO_PRED   = 'No prediction'

# Error messages
BAD_CHROM  = "Error: unexpected chromosome"
BAD_POS    = "Error: unexpected position"
BAD_BASE   = "\nError: reference and mutant nucleotides must both be ACGT\n%s\n\n"
BAD_MUTANT = "\nError: reference and mutant nucleotides must be different\n%s\n\n"
TABIX_WARN = "** Warning: cannot find tabix executable in your path\n"

DEFAULT_PRED = ['', '', 'No prediction found']

def confidence(s, thresh) :
    """Returns the confidence level for (neutral, low-confidence or high-confidence)
    for the given p-value string using the given threshold.  If the string is invalid,
    returns 'no prediction'"""
    try :
        x = float(s)
        if x >= thresh :
            return HIGH_CONF
        elif x >= DEFAULT_THRESH :
            return LOW_CONF
        else :
            return NEUTRAL
    except Exception :
        return NO_PRED

def findFile(name, path, delim=':') :
    """Finds the first instance of a file name in the given path string."""
    paths = path.split(delim)
    for p in paths :
        filePath = os.path.join(p, name)
        if os.path.exists(filePath) and os.path.isfile(filePath) :
            return filePath

def getPrediction(recordList, query, predictionType) :
    """Returns a full prediction result for the given record list and query."""
    (chrom,pos,reference,mutant) = query
    result = list(DEFAULT_PRED)
    if not recordList :
        return result
    for record in recordList.split("\n"):
        if not record: continue
        parts  = record.strip().split("\t")
        result = list(DEFAULT_PRED)
        if parts[0] != chrom:
            result[-1] = BAD_CHROM
            break
        elif int(parts[1]) != pos :
            result[-1] = BAD_POS
            break
        elif parts[2] != reference:
            result[-1] = "Error: unexpected reference '%s' at %s:%d" % (reference, chrom, pos)
            break
        elif parts[3] == mutant: # SUCCESS!
            if predictionType == CODING_PRED :
                result = [parts[4], '', confidence(parts[4], CODING_HIGH_THRESH)]
            else :
                result = ['', parts[4], confidence(parts[4], NONCODING_HIGH_THRESH)]
            break
    return result

def runTabix(db, query, predictionType) :
    """Spawns a subprocess to run tabix and query the given database."""
    (chrom,pos,reference,mutant) = query
    cmd         = "tabix %s %s:%d-%d" % (db, chrom, pos, pos+1)
    proc        = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result, err = proc.communicate()
    if err: raise IOError("** Error running %s query for %s on %s" % (predictionType, queryString, db))
    return result

def timeString(s, format_string='%X') :
    """Returns the input string with user-readable a timestamp prefix."""
    timestamp = time.strftime(format_string, time.localtime())
    result    =  '%s %s' % (timestamp, s)
    return result

def validateFile(path) :
    """Standard method for validating file paths."""
    if not path :
        raise Exception("'%s' is not a valid file path; exiting." % path)
    if not os.path.exists(path) :
        raise Exception("File '%s' not found; exiting." % path)

USAGE = """%prog query-file [options]

Predict the oncogenic potential of single nucleotide variants (SNVs).  The query
file must be a list of queries that use the following format:

chromosome,position,reference,mutant

Example:

1,69094,G,A
11,168961,T,A
18,119888,G,A"""
# Establish command-line options:
parser = optparse.OptionParser(usage=USAGE)
parser.add_option('-c', dest='cdb',     default=DEFAULT_CODING_DB,     help='CScape coding database [default: %default]')
parser.add_option('-n', dest='ndb',     default=DEFAULT_NONCODING_DB,  help='CScape noncoding database [default: %default]')
parser.add_option('-o', dest='output',  default=None,                  help='Output file [default: stdout]')
parser.add_option('-v', dest='verbose', default=False,                 help='Verbose mode [default: %default]', action='store_true')
opts, args = parser.parse_args(sys.argv[1:])

MIN_ARGS = 1
if len(args) != MIN_ARGS :
    parser.print_help()
    sys.exit(1)

queryFile = args[0]

for f in [queryFile,opts.cdb,opts.ndb] :
    validateFile(f)

outStream = sys.stdout if not opts.output else open(opts.output,'w')
outStream.write('%s\n' % '\t'.join(['# Chromosome', 'Position', 'Reference', 'Mutant', 'Coding', 'Noncoding', 'Remark']))

# Check tabix executable
try :
    tabixExe = findFile('tabix', os.environ['PATH'])
    if not tabixExe :
        sys.stderr.write(TABIX_WARN)
except KeyError :
    sys.stderr.write(TABIX_WARN)

# Validate all queries
queryList = []
for queryString in open(queryFile,'r') :
    queryString = queryString.strip()
    if not queryString or queryString.startswith("#"): continue

    # Ensure chromosome and nucleotides are upper case
    queryParts = queryString.upper().split(",")

    # validate query format
    if len(queryParts) != 4 : raise ValueError("Error: invalid query format '%s'" % queryString)

    try :
        pos = int(queryParts[1])
    except:
        raise ValueError("Error: invalid position %d in '%s'" % (queryParts[1], queryString))

    chrom     = queryParts[0].strip().replace('CHR','')
    reference = queryParts[2]
    mutant    = queryParts[3]

    if reference not in NUCLEOTIDES :
        sys.stderr.write(BAD_BASE % queryString)
        sys.exit(1)

    if mutant not in NUCLEOTIDES :
        sys.stderr.write(BAD_BASE % queryString)
        sys.exit(1)

    if reference == mutant :
        sys.stderr.write(BAD_MUTANT % queryString)
        sys.exit(1)

    query = (chrom.strip(), pos, reference, mutant)
    queryList.append(query)

# run queries
for query in queryList :
    # first try coding prediction ...
    predType = CODING_PRED
    data     = runTabix(opts.cdb, query, predType)
    if not data : # try noncoding prediction ...
        predType = NONCODING_PRED
        data     = runTabix(opts.ndb, query, predType)

    # get prediction columns
    predList = getPrediction(data, query, predType)

    outStream.write('%s\t%d\t%s\t%s\t' % query)
    outStream.write('%s\n' % '\t'.join(predList))
