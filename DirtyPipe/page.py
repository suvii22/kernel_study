import gdb

class PageAddressCommand(gdb.Command):
    """Calculate the virtual address of a page struct in Linux kernel.

    Usage: page_address <page>
    where <page> is the address of a 'struct page *'.
    """

    def __init__(self):
        super(PageAddressCommand, self).__init__("page_address", gdb.COMMAND_DATA, gdb.COMPLETE_EXPRESSION)

    def invoke(self, arg, from_tty):
        # Parse the argument to get the page address
        args = gdb.string_to_argv(arg)
        if len(args) != 1:
            raise gdb.GdbError("page_address command requires exactly one argument")

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
PageAddressCommand()