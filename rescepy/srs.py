# Author: Joseph Wiseman <joswiseman@outlook>
# URL: https://github.com/d2yes/rescepy/
#
# This file is part of rescepy.
#

import os,resample,subprocess

class SRS(object):
    def __init__(self, filename, binary=None):
        self.filename = filename
        if binary == None:
            if os.name == 'posix':
                self.binary = '/usr/bin/srs'
            elif os.name == 'nt':
                self.binary = 'srs.exe'
        else:
            self.binary = binary

    def recreate(self, infile, outdir='Sample' + os.sep):
        if not os.path.isdir(outdir):
            try:
                os.makedirs(outdir)
            except:
                if len(str(sys.exc_info()[1])) > 0:
                    print sys.exc_info()[1]
                return False

        sp = subprocess.Popen('%s \'%s\' \'%s\' -o \'%s\' -y' % (self.binary, self.filename, infile, outdir), shell=True, stdin=subprocess.PIPE)
        sp.communicate()

        return True if sp.returncode == 0 else False

    def info(self):
        rgft = resample.get_file_type(self.filename)
        if rgft == 'Unknown':
            print '\'%s\' is unknown file type.' % (self.filename)
            return False

        rscf = resample.sample_class_factory(rgft)
        data, tracks = rscf.load_srs(self.filename)

        return (data.name, data.size, '%X' % (data.crc32 & 0xFFFFFFFF))