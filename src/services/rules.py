class GroupRules:
    """User can't be a member of both groups"""

    CONTRADICTORY = [
        {"Developer", "Owner"},
        {"ExampleGroup1", "ExampleGroup2"},
        {"ExampleGroup3", "ExampleGroup4"},
    ]
