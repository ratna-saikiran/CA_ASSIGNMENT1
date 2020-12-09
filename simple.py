from __future__ import print_function
from __future__ import absolute_import
import m5
from m5.objects import *
from m5.params import *
from caches import *
from optparse import OptionParser
from os import getcwd
#from common import Options
#m5.util.addToPath('/home/rathna/gem5/configs/common')
parser = OptionParser()
parser.add_option("-o", "--options", default="",
                      help="""The options to pass to the binary, use " "
                              around the entire string""")
parser.add_option('--l1i_size', help="L1 instruction cache size")
parser.add_option('--l1d_size', help="L1 data cache size")
parser.add_option('--l2_size', help="Unified L2 cache size")


(options, args) = parser.parse_args()
isa = str(m5.defines.buildEnv['TARGET_ISA']).lower()
system = System()
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]
system.cpu = TimingSimpleCPU()
system.membus = SystemXBar()

system.cpu.icache = L1ICache(options)
system.cpu.dcache = L1DCache(options)

system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

system.l2bus = L2XBar()

system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)
system.l2cache = L2Cache(options)
system.l2cache.connectCPUSideBus(system.l2bus)

system.l2cache.connectMemSideBus(system.membus)


system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.master
system.cpu.interrupts[0].int_master = system.membus.slave
system.cpu.interrupts[0].int_slave = system.membus.master
system.system_port = system.membus.slave
system.mem_ctrl = DDR3_1600_8x8()
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.master


# Create a process for a simple "Hello World" application
process = Process()
# Set the command/home/rathna/Desktop/CA_1/MiBench/automotive/susan
# cmd is a list which begins with the executable (like argv)
process.cmd = ['/home/rathna/gem5/configs/tutorial/susan/susan','/home/rathna/gem5/configs/tutorial/susan/input_small.pgm','/home/rathna/gem5/configs/tutorial/susan/output_small.smoothing.pgm']
process.cwd=os.getcwd()
#process.input=('cin',''
# Set the cpu to use the process as its workload and create thread contexts
system.cpu.workload = process
system.cpu.createThreads()

# set up the root SimObject and start the simulation
root = Root(full_system = False, system = system)
# instantiate all of the objects we've created above
m5.instantiate()

print("Beginning simulation!")
print(process.cwd)
exit_event = m5.simulate()
print('Exiting @ tick %i because %s' % (m5.curTick(), exit_event.getCause()))







