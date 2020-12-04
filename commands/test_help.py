import unittest
import help_page
import io
import sys

class MyhelpCommandsTests(unittest.TestCase):
    def test_help_sheet(self):
        output = sys.__stdout__
        output = help_page.help_sheet()
        
        self.assertEqual(output, """
 CODE-CLINIC'S HELP COMMANDS

 utilization: clinic [COMMAND] [ARGUMENTS]
 help usage: clinic [-h , --help] & [book help]
 
     All the code clinics commands:
     
     Viewing:
            -v [OPTION]                Views the bookings for 7 days     
              e.g 'clinic -v 8'
     
     Volunteering/Opening:
            -o [datetime]              Creates a volunteer slot
              e.g 'clinic -o 27-11-2020'
            
     Booking:
            -b [slot ID]               Books an availeble slot
              e.g 'clinic -b 5er7'
            
     Cancel:
            -c [slot ID]               Cancels available slot specified
             e.g 'clinic -c 5er7'
            
     Options for booking:
            -n | -b [slot ID] [OPTION] [MESSAGE]          Adds notes to your slot
            -a | -b [slot ID] [OPTION] [FOLDER.NAME]      Attach a folder to your slot
       """)

if __name__ == "__main__":
    
    unittest.main()