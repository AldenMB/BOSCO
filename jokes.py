import bosco

def generalized_lightbulb():
    bosco.say(
        'How many members of a given disparaged social group does it take to change a lightbulb?'
        ).join()
    #how many?
    bosco.wait()
    bosco.say(
        'N plus one, where one member changes the lightbulb and N behave in a manner stereotypical of that social group.'
        ).join()
    bosco.sting().join()

def generalized_knock_knock():
    bosco.say(
        'Knock knock'
        ).join()
    # who is there?
    bosco.wait()
    bosco.say(
        "A person's first name which also sounds like part of a common phrase."
        ).join()
    # A person's first name which also sounds like part of a common phrase who?
    bosco.wait()
    bosco.say(
        "The complete common phrase."
        ).join()
    bosco.sting().join()