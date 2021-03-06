import logging
import os
import subprocess

PLAYBACK_CONFIG_TEMPLATE="""
# Configuration file for playing back Telescope Operating System Simulator
# (tossim) and Correlator Simulator (corrsim).
#
# Parameters for both
#
# Correlator cycle time in seconds
playback.period = 5

# Data input mode
# TO BE DEPRECATED
# For the time being, use "expand" only.
#playback.input_mode = zero
playback.input_mode = expand


#----------------------------------------------------------------------
# Telescope Operating System Simulator Configuration
#
# For transmission (using ICE)
playback.tossim.ice.locator_host = localhost
playback.tossim.ice.locator_port = 4061
playback.tossim.icestorm.topicmanager = IceStorm/TopicManager@IceStorm.TopicManager
playback.tossim.icestorm.topic = metadata

# Transmission delay in microsecond
playback.tossim.delay = 5000000
#playback.tossim.delay = 0

# Simulate random failures to send metadata message. A value of of 0.0
# results in no failures, while 1.0 results in all sends failing.
# (Default: 0.0)
#playback.tossim.random_metadata_send_fail = 0.1


#----------------------------------------------------------------------
# Correlator Simulator configuration
#
# Total number of antennas to be simulated.
# If the number is greater than that in measurement set, data will be 
# copied from existing antennas.
# Range: 1 (default) to 36 (max for ASKAP)
playback.corrsim.n_antennas = 36

# Total number of coarse channels to be simulated.
# Ideally 304 (default), but current hardware is limited at 300.
# If the number is greater than that in measurement set, data will be 
# copied from existing coarse channels.
# single card case - just four coarse channels
playback.corrsim.n_coarse_channels = 4

# Division of coarse channel into fine channels
# Default: 54
playback.corrsim.n_channel_subdivision = 54

# Coarse channel bandwidth (Hertz)
# Default: 1 MHz
playback.corrsim.coarse_channel_bandwidth = 1000000

# Measurement set used as input for simulation
playback.corrsim.dataset = {playbackdataset}

# Local host for transmission
playback.corrsim.out.hostname = localhost

# Reference port for transmission.
# If multiple ports are used, this is the first port
playback.corrsim.out.port = 3000

# Delay in transmission between different time groups (microsecond)
playback.corrsim.delay = 5000000

# TO ADD LATER: Failure pattern (make sure repeatable, ie. not random)
#
# NOTE
# - In this version (ADE version), baseline map is computed automatically.
#   In previous version (BETA version), such map must be provided 
#   explicitly in this file.
#
"""

def writeFromTemplate(path, template, params):
    with open(path, "w") as f:
        f.write(template.format(**params))

def writePlaybackConfig(path, params):
    writeFromTemplate(path, PLAYBACK_CONFIG_TEMPLATE, params)

class Playback:
    def __init__(self, workingdirectory):
        if "AIPSPATH" not in os.environ:
            logging.debug("Adding AIPSPATH to environment.")
            os.environ["AIPSPATH"] = "%s/Code/Base/accessors/current" % os.environ["ASKAP_ROOT"]

        self.workingdirectory = workingdirectory

        if not os.path.exists(workingdirectory):
            os.mkdir(workingdirectory)

        self.playbackConfigPath = "%s/playback.in" % workingdirectory
        self.playbackLogPath = "%s/playback.out" % workingdirectory
        
    def playback(self, dataset):
        params = {'playbackdataset': dataset}

        writePlaybackConfig(self.playbackConfigPath, params)

        playbackLog = open(self.playbackLogPath, "w")

        logging.debug("Command is 'timeout -s 9 10m mpirun -np 2 %s/Code/Components/Services/correlatorsim/current/apps/playbackADE.sh -c %s'" % (os.environ['ASKAP_ROOT'], self.playbackConfigPath))
        self.proc = subprocess.Popen(['timeout', '-s', '9', '10m', 'mpirun', '-np', '2', '%s/Code/Components/Services/correlatorsim/current/apps/playbackADE.sh' % os.environ['ASKAP_ROOT'], '-c', self.playbackConfigPath], stdout=playbackLog)
        #self.proc = subprocess.Popen(['timeout', '-s', '9', '10m', 'mpirun', '-np', '2', '%s/Code/Components/Services/correlatorsim/current/apps/playbackADE.sh' % os.environ['ASKAP_ROOT'], '-c', self.playbackConfigPath])
        logging.debug("playback proc pid is %d." % self.proc.pid)
        if self.proc.poll():
            logging.debug("playback has terminated already!")

    def wait(self):
        self.proc.wait()

    def abort(self):
        self.proc.kill()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(threadName)s, %(module)s: %(message)s')

    from myice import MyIce

    myice = MyIce("testbed_data")
    myice.start()

    playback = Playback("testbed_data")
    playback.playback("../data/ade1card.ms")
    playback.wait()

    myice.stop()

