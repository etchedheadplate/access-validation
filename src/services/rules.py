class GroupRules:
    """User can't be a member of both groups"""

    CONTRADICTORY = [
        {"Frontend Developer", "Backend Developer"},
        {"ExampleGroup1", "ExampleGroup2"},
        {"ExampleGroup3", "ExampleGroup4"},
    ]


class PermissionRules:
    """User from from lower group can't have any permissions of higher group"""

    CONTRADICTORY = [
        {"low": "Tester", "high": "Owner"},
        {"low": "ExampleGroup5", "high": "ExampleGroup6"},
        {"low": "ExampleGroup7", "high": "ExampleGroup8"},
    ]
