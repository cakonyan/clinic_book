def help_sheet():
    commands = """
 CODE-CLINIC'S HELP COMMANDS

 utilization: clinic [COMMAND] [ARGUMENTS]
 help usage: clinic [-h , --help] & [book help]
 
     All the code clinics commands:
     
     Viewing:
            -v [OPTION]                   Views the bookings for 7 days     
              e.g 'clinic -v'
     
     Volunteering/Opening:
            -o [datetime]                 Creates a volunteer slot
            -n | -o [datetime] [MESSAGE]  Adds notes to your slot
              e.g 'clinic -o'
            
     Booking:
            -b [slotId]                   Books an availeble slot
            
              e.g 'clinic -b'
              e.g 'clinic -b Recursion'
            
     Cancel:
            -c [slotId]                   Cancels available slot specified
              e.g 'clinic -c'
            
     Options for booking:
            
       """
       
    return commands


