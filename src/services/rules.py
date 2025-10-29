from dataclasses import dataclass


@dataclass
class GroupRules:
    CONTRADICTORY = [
        {"Developer", "DB Admin"},
        {"ExampleGroup1", "ExampleGroup2"},
        {"ExampleGroup3", "ExampleGroup4"},
    ]


@dataclass
class PermissionRules:
    CONTRADICTORY = [
        {"Developer", "DB Admin"},
        {"ExampleGroup1", "ExampleGroup2"},
        {"ExampleGroup3", "ExampleGroup4"},
    ]
