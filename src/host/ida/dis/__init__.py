import idaapi

import ir
import ir.intel

from . import intel

def disassembler_for_arch(arch_name=None):
  """ find the architecture currently in use for this IDB. """

  if not arch_name:
    arch_name = idaapi.get_file_type_name()

  if '386' in arch_name:
    print 'Architecture: 32-bit intel.'
    return (ir.IR_INTEL_x86, ir.intel.ir_intel_x86, intel.disassembler)
  elif 'x86-64' in arch_name:
    print 'Architecture: 64-bit intel.'
    return (ir.IR_INTEL_x64, ir.intel.ir_intel_x64, intel.disassembler)

  raise RuntimeError("Don't know which arch to choose for %s" % (repr(arch_name), ))

def create(arch_name=None):
  """ Find the correct disassembler module for this host.

  Return a new instance of a disassembler made up of the generic
  architecture support (from ir/*.py) and the specific host disassembler
  for this architecture.
  """

  ir_id, ir_cls, dis_cls = disassembler_for_arch(arch_name)

  class disassembler(dis_cls, ir_cls): # disassembler (host) class must be left-most.
    def __init__(self, ir_id):
      self.ir_id = ir_id
      dis_cls.__init__(self)
      ir_cls.__init__(self)
      return

  dis = disassembler(ir_id)

  return dis

