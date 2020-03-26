"""
A file where all constants are defined
"""
#Bot token
token = "mysuperstylishtoken"

#Prefix for invoking a command
cmd_prefix = '$'

#Text in the "Raise your hand" message
raise_your_hand_text = "Raise your hand !"

#The emoji that the bot adds as a reaction (rasied hand default)
raised_hand_emoji = b'\xe2\x9c\x8b'

#The prefix that is added to the nicknames
#A dot lets the people who raises their hand to be brought up in the list (since discord sorts nicknames in alphabetical order)
raised_hand_prefix = "."

#Future feature (:
#TODO role_restriction_id = 
#Error returned when someone requests a raise your hand message when the previous wasn't ended
multiple_rmh_messages_error = "You can only send one raise my end message, to end the previous, type " + cmd_prefix + "e"

#TODO : clean this out of here
raised_hand_emoji = raised_hand_emoji.decode("utf8")