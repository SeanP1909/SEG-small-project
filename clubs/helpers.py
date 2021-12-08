#Create the content of the dropdown menu for the experience atribute of the user model.
def experienceChoices():
    EXPERIENCE_LEVELS = (
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
        ("master", "Master"),
        ("professional", "Professional")
    )
    return EXPERIENCE_LEVELS

def match_result_choices():
    return (
        ("first_win", "1:0"),
        ("second_win", "0:1"),
        ("draw", "1/2:1/2")
    )