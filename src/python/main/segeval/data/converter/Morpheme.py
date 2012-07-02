'''
Converts morphological segmentation input into segmentation masses to be
evaluated.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
#===============================================================================
# Copyright (c) 2012, Chris Fournier
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the author nor the names of its contributors may
#       be used to endorse or promote products derived from this software
#       without specific prior written permission.
#       
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#===============================================================================
import csv
from .. import Dataset, DataIOError, name_from_filepath
from ..JSON import FIELD_HAS_REFERENCE_CODER
from ..TSV import DEFAULT_DELIMITER


CODER_REFERENCE = 'reference'


def input_morphemes(tsv_filename, reference_coder=False,
                    delimiter=DEFAULT_DELIMITER):
    '''
    Load a morphological segmentation TSV file for a single coder representing
    many items.
    
    :param tsv_filename: path to the mass file containing words and morphological
                         segmentations.
    :param delimiter:    the delimiter used when reading a TSV file (by default,
                         a tab, but it can also be a comma, whitespace, etc.
    :type tsv_filename: str
    :type delimiter: str
    
    :returns: Segmentation mass codings.
    :rtype: :func:`dict`
    '''
    # pylint: disable=R0914
    # List version of file
    dataset = Dataset()
    coder = CODER_REFERENCE if reference_coder else \
        name_from_filepath(tsv_filename)
    if reference_coder:
        dataset.properties[FIELD_HAS_REFERENCE_CODER] = True
        
    # Open file
    csv_file = open(tsv_filename, 'rU')
    # Read in file
    try:
        reader = csv.reader(csv_file, delimiter=delimiter)
        for row in reader:
            # Read data
            item = None
            for j, col in enumerate(row):
                if j == 0:
                    # First col is the word (i.e., item)
                    item = str(col)
                elif j == 1:
                    # First col is the morphological segmentation (i.e., masses)
                    options = [option.strip() for option in col.split(',')]
                    for i, option in enumerate(options):
                        current_coder = coder if i == 0 else coder + str(i + 1)
                        # Create coder if it does not exist
                        if item not in dataset:
                            dataset[item] = dict()
                        # Convert into segment mass
                        dataset[item][current_coder] = \
                            [len(morpheme) for morpheme in option.split(' ')]
    # pylint: disable=C0103
    except Exception as exception:
        raise DataIOError('Error occurred processing file: %s' \
                                      % tsv_filename, exception)
    finally:
        csv_file.close()
    return dataset

