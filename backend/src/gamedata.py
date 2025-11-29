WORLD = {
    "intro": {
        "title": "Echoes of the Nebula",
        "desc": (
            "You awaken amid the wreckage of your downed starship. Sparks shower from torn "
            "consoles, and the alien moon’s violet sky hums with strange energy. The ground is "
            "soft and bioluminescent, pulsing beneath your boots. Nearby, a damaged escape pod "
            "lies half-buried in the soil, and to the north, a narrow trail leads toward a glowing forest."
        ),
        "choices": {
            "inspect_pod": {
                "desc": "Inspect the damaged escape pod.",
                "result_scene": "escape_pod",
            },
            "scan_area": {
                "desc": "Use your limited suit systems to scan the crash site.",
                "result_scene": "distress_signal",
            },
            "go_forest": {
                "desc": "Head toward the glowing forest trail.",
                "result_scene": "glowing_forest",
            },
        },
    },

    "escape_pod": {
        "title": "Escape Pod Examination",
        "desc": (
            "The escape pod is cracked open, its power core flickering weakly. Inside, you find a "
            "half-functional scanning visor and a small energy cell humming faintly."
        ),
        "choices": {
            "take_items": {
                "desc": "Take the visor and energy cell.",
                "result_scene": "distress_signal",
                "effects": {
                    "add_inventory": "scanning_visor",
                    "add_journal": "Recovered damaged scanning visor.",
                },
            },
            "leave_pod": {
                "desc": "Leave the pod and return to the crash site.",
                "result_scene": "intro",
            },
        },
    },

    "distress_signal": {
        "title": "Signal Flicker",
        "desc": (
            "Your visor (even in damaged state) picks up a faint distress beacon northwest of here. "
            "The signal fluctuates with bursts of static, as if obstructed by dense structures—or something alive."
        ),
        "choices": {
            "follow_signal": {
                "desc": "Move toward the distress beacon.",
                "result_scene": "alien_ruins",
            },
            "ignore_signal": {
                "desc": "Head instead toward the glowing forest.",
                "result_scene": "glowing_forest",
            },
        },
    },

    "glowing_forest": {
        "title": "The Glowing Woods",
        "desc": (
            "Soft blue trees shimmer with internal light. Strange insect-like drones buzz overhead. "
            "A path of crushed foliage suggests something large recently passed through."
        ),
        "choices": {
            "investigate_tracks": {
                "desc": "Examine the large tracks.",
                "result_scene": "hostile_creature",
            },
            "take_shard": {
                "desc": "Collect a crystalline shard from a glowing tree.",
                "result_scene": "shard_taken",
                "effects": {
                    "add_inventory": "crystalline_shard",
                    "add_journal": "Collected a crystalline shard with unknown energy.",
                },
            },
            "retreat": {
                "desc": "Return to the crash site.",
                "result_scene": "intro",
            },
        },
    },

    "shard_taken": {
        "title": "Energy Surge",
        "desc": (
            "The shard pulses warmly in your hand. Your visor briefly stabilizes, highlighting an underground "
            "structure beneath the forest floor—likely connected to the ruins hinted in the distress signal."
        ),
        "choices": {
            "descend_structure": {
                "desc": "Search for an entrance to the underground structure.",
                "result_scene": "crystalline_chamber",
            },
            "return_forest": {
                "desc": "Head deeper into the forest.",
                "result_scene": "glowing_forest",
            },
        },
    },

    "hostile_creature": {
        "title": "Predator Encounter",
        "desc": (
            "A sinewy, quadrupedal creature emerges—its eyes glowing amber, its body armored with crystalline plates. "
            "It lets out a low, resonant growl. Your suit warns of elevated threat levels."
        ),
        "choices": {
            "stand_ground": {
                "desc": "Stand your ground and confront it.",
                "result_scene": "artifact_room",
                "effects": {
                    "add_journal": "Survived confrontation with crystalline predator.",
                },
            },
            "run_back": {
                "desc": "Retreat toward the crash site.",
                "result_scene": "intro",
            },
        },
    },

    "alien_ruins": {
        "title": "Ancient Ruins",
        "desc": (
            "Jagged metal spires rise from the earth, humming with old power. A triangular entryway pulses with faint "
            "light. Inside lies a long corridor etched with alien runes—some glow when you approach."
        ),
        "choices": {
            "enter_ruins": {
                "desc": "Enter the alien corridor.",
                "result_scene": "artifact_room",
            },
            "circle_ruins": {
                "desc": "Circle the ruins for another way in.",
                "result_scene": "crystalline_chamber",
            },
            "return_signal": {
                "desc": "Follow the distress beacon’s direction.",
                "result_scene": "extraction_point",
            },
        },
    },

    "crystalline_chamber": {
        "title": "Crystal Heart",
        "desc": (
            "You descend into a cavern where the very stone vibrates with weak energy. A floating stabilizer field contains "
            "a small alien artifact shaped like a twisting loop."
        ),
        "choices": {
            "take_artifact": {
                "desc": "Retrieve the alien artifact.",
                "result_scene": "extraction_point",
                "effects": {
                    "add_inventory": "alien_artifact",
                    "add_journal": "Retrieved an alien artifact emitting low-frequency pulses.",
                },
            },
            "leave_chamber": {
                "desc": "Leave and head toward the ruins.",
                "result_scene": "alien_ruins",
            },
        },
    },

    "artifact_room": {
        "title": "Control Nexus",
        "desc": (
            "Deep within the ruins lies a circular chamber. In the center floats a control console, inactive. "
            "Your visor flickers—perhaps the artifact or shard could activate it."
        ),
        "choices": {
            "use_shard": {
                "desc": "Try using the crystalline shard to power the console.",
                "result_scene": "extraction_point",
            },
            "use_artifact": {
                "desc": "Place the alien artifact on the console.",
                "result_scene": "extraction_point",
            },
            "leave_room": {
                "desc": "Retreat toward the forest.",
                "result_scene": "glowing_forest",
            },
        },
    },

    "extraction_point": {
        "title": "Extraction Beacon",
        "desc": (
            "Your visor stabilizes, revealing a tall beacon spire ahead. The distress signal converges here. "
            "A landing zone glows faintly—if powered, rescue may be possible."
        ),
        "choices": {
            "activate_beacon": {
                "desc": "Try to activate the beacon.",
                "result_scene": "resolution_good",
                "effects": {
                    "add_journal": "Activated extraction beacon.",
                },
            },
            "fail_sequence": {
                "desc": "Attempt override without proper components.",
                "result_scene": "resolution_bad",
            },
        },
    },

    "resolution_good": {
        "title": "Rescue Achieved",
        "desc": (
            "A patrol dropship descends through the violet clouds. You are lifted aboard, artifact in hand. "
            "Your survival—and discoveries—may shape future missions to this strange moon."
        ),
        "choices": {
            "end_session": {
                "desc": "End the session and return to crash site.",
                "result_scene": "intro",
            }
        },
    },

    "resolution_bad": {
        "title": "Signal Collapse",
        "desc": (
            "The beacon overloads, sending a shockwave across the valley. Darkness sweeps in as your visor fails. "
            "Your mission ends here—for now."
        ),
        "choices": {
            "restart": {
                "desc": "Restart from the beginning.",
                "result_scene": "intro",
            }
        },
    },
}