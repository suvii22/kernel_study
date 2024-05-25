import gdb

class GenericStruct:
    def __init__(self, val):
        self.val = val

    def get_member(self, member_name):
        return self.val[member_name]

    def print_member(self, member_name):
        print(f"> '{member_name}': {self.get_member(member_name)}")

class Pipe(GenericStruct):
    stype = gdb.lookup_type("struct pipe_inode_info")
    ptype = stype.pointer()

    def _print_info(self):
        self.print_member("head")
        self.print_member("tail")
        self.print_member("ring_size")
        self.print_member("bufs")

class PipeBuffer(GenericStruct):
    stype = gdb.lookup_type("struct pipe_buffer")
    ptype = stype.pointer()
    flags = {
        "PIPE_BUF_FLAG_LRU": 0x01,
        "PIPE_BUF_FLAG_ATOMIC": 0x02,
        "PIPE_BUF_FLAG_GIFT": 0x04,
        "PIPE_BUF_FLAG_PACKET": 0x08,
        "PIPE_BUF_FLAG_CAN_MERGE": 0x10,
        "PIPE_BUF_FLAG_WHOLE": 0x20,
    }

    def sym_flags(self):
        tmp = []
        for key, value in self.flags.items():
            if int(self.get_member("flags")) & value != 0:
                tmp.append(key)
        if len(tmp) == 0:
            return "none"
        return " | ".join(tmp)

    def _print_info(self):
        # TODO add print_misc to parent
        self.print_member("page")
        self.print_member("offset")
        self.print_member("len")
        self.print_member("ops")
        print("> 'flags': " + self.sym_flags())

class PrintPipeCommand(gdb.Command):
    """Print the information of a struct pipe_inode_info"""

    def __init__(self):
        super().__init__("print-pipe", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        arg = arg.strip()
        if not arg:
            print("Usage: print-pipe <address>")
            return

        try:
            pipe = Pipe(gdb.parse_and_eval(arg).cast(Pipe.ptype))
            pipe._print_info()
        except gdb.error as e:
            print(f"Error: {e}")

class PrintPipeBufferCommand(gdb.Command):
    """Print the information of a struct pipe_buffer"""

    def __init__(self):
        super().__init__("print-pipe-buffer", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        arg = arg.strip()
        if not arg:
            print("Usage: print-pipe-buffer <address>")
            return

        try:
            pipe_buffer = PipeBuffer(gdb.parse_and_eval(arg).cast(PipeBuffer.ptype))
            pipe_buffer._print_info()
        except gdb.error as e:
            print(f"Error: {e}")

class p2vCommand(gdb.Command):
    """Calculate the virtual address of a page struct in Linux kernel.

    Usage: p2v <page>
    where <page> is the address of a 'struct page *'.
    """

    def __init__(self):
        super(p2vCommand, self).__init__("p2v", gdb.COMMAND_DATA, gdb.COMPLETE_EXPRESSION)

    def invoke(self, arg, from_tty):
        # Parse the argument to get the page address
        args = gdb.string_to_argv(arg)
        if len(args) != 1:
            raise gdb.GdbError("p2v command requires exactly one argument")

        page = gdb.parse_and_eval(args[0])

        # Calculate the virtual address using the method from the Page class
        vmemmap_base = int(gdb.parse_and_eval("vmemmap_base"))
        page_offset_base = int(gdb.parse_and_eval("page_offset_base"))
        page = int(page)
        page_size = gdb.lookup_type("struct page").sizeof
        page_shift = 12  # Typically 4096 bytes per page

        virtual_address = (
            int((page - vmemmap_base) / page_size) << page_shift
        ) + page_offset_base

        # Print the result
        gdb.write("Virtual address: 0x{0:x}\n".format(virtual_address))

# Register the command with GDB
p2vCommand()
PrintPipeCommand()
PrintPipeBufferCommand()
