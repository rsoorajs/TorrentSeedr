import time
from src.objs import *

#: Flood prevention
def floodControl(message, userLanguage):
    userId = message.from_user.id
    
    if userId == config['adminId']:
        return True

    #! If the user is not banned
    if not dbSql.getSetting(userId, 'blockTill', table='flood') - int(time.time())  > 0:
        lastMessage = dbSql.getSetting(userId, 'lastMessage', table='flood')

        currentTime = int(time.time())

        #! Spam detected
        if currentTime - lastMessage < 1:
            #! If the user is already warned, block for 5 minutes
            if dbSql.getSetting(userId, 'warned', table='flood'):
                bot.send_message(message.chat.id, language['blockedTooFast'][userLanguage])
                dbSql.setSetting(userId, 'blockTill', int(time.time())+300, table='flood')
                dbSql.setSetting(userId, 'warned', 0, table='flood')
            
            #! If the user is not warned, warn for the first time
            else:
                bot.send_message(message.chat.id, language['warningTooFast'][userLanguage])
                dbSql.setSetting(userId, 'warned', 1, table='flood')
            
            return False
        
        #! No spam
        else:
            dbSql.setSetting(userId, 'lastMessage', int(time.time()), table='flood')
            return True