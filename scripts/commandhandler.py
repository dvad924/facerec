# module for dealing with commands sent from a UI and setting
# the correct settings object

def commandhandler( msg ):
    config = {}
    
    parse_cmd( msg.data, config )

    return config
    
    
    

def parse_cmd( msg, settings ):
    
    msg_parts = msg.split(':')
    if ( msg_parts[0] == 'label' ):
        settings['label'] = msg_parts[1]
        settings['store'] = True

    elif ( msg_parts[0] == 'stop' ):
        settings['label'] = None
        settings['store'] = False
    
