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