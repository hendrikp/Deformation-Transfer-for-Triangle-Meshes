import os
import sys;

dname = os.path.dirname(os.path.realpath(__file__))

sys.path.append(dname) # fix relative module search
os.chdir(dname) # FIXME: workaround for working directory, otherwise the config files arent found