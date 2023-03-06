# Imports
from tools.Debug import Debug
import platform
import subprocess


class Ping:

    def command_ping(self, host_or_ip, packets=1, timeout=1000):

        """ Calls system 'ping' command, returns True if ping succeeds.
        Required parameter: host_or_ip (str, address of host to ping)
        Optional parameters: packets (int, number of retries), timeout (int, ms to wait for response)
        Does not show any output, either as popup window or in command line.
        Python 3.5+, Windows and Linux compatible
        """

        # Debug/
        Debug.log("Ping in address: {0} | {1} packets | Timeout {2}.".format(str(host_or_ip), str(packets), str(timeout)))

        # The ping command is the same for Windows and Linux, except for the "number of packets" flag.
        if platform.system().lower() == "windows":

            # Create command;
            command = ['ping', '-n', str(packets), '-w', str(timeout), host_or_ip]

            # Run parameters: capture output, discard error messages, do not show window;
            result = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                    stderr=subprocess.DEVNULL, creationflags=0x08000000)

            # 0x0800000 is a windows-only Popen flag to specify that a new process will not create a window.
            # On Python 3.7+, you can use a subprocess constant:
            # result = subprocess.run(command, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
            # On windows 7+, ping returns 0 (ok) when host is not reachable; to be sure host is responding,
            # we search the text "TTL=" on the command output. If it's there, the ping really had a response.
            return result.returncode == 0 and b'TTL=' in result.stdout

        else:

            # Create command;
            command = ['ping', '-c', str(packets), '-w', str(timeout), host_or_ip]

            # Run parameters: discard output and error messages;
            result = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL)

            return result.returncode == 0


# if __name__ == "__main__":
#
#     # Objects;
#     ping = Ping()
#
#     # Vars;
#     address = "1.1.189.29"
#
#     # Create ping command;
#     ping_result = ping.command_ping(address, 5, 1000)
#
#     # Debug
#     print("Ping result: {0}".format(str(ping_result)))
