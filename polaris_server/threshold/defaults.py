default_thresholds = {
    "2G": [
        {
            "name": "rxlev",
            "signal_type": "quantity",
            "levels": [
                {"level": 1, "color": "#FF0000", "min": -110, "max": -100},
                {"level": 2, "color": "#FFFF00", "min": -100, "max": -80},
                {"level": 3, "color": "#008000", "min": -80, "max": -50},
            ],
        }
    ],
    "3G": [
        {
            "name": "rscp",
            "signal_type": "quantity",
            "levels": [
                {"level": 1, "color": "#FF0000", "min": -120, "max": -110},
                {"level": 2, "color": "#FFFF00", "min": -110, "max": -90},
                {"level": 3, "color": "#008000", "min": -90, "max": -60},
            ],
        }
    ],
    "4G": [
        {
            "name": "rsrp",
            "signal_type": "quantity",
            "levels": [
                {"level": 1, "color": "#FF0000", "min": -140, "max": -120},
                {"level": 2, "color": "#FFA500", "min": -120, "max": -110},
                {"level": 3, "color": "#008000", "min": -110, "max": -80},
            ],
        },
        {
            "name": "rsrq",
            "signal_type": "quality",
            "levels": [
                {"level": 1, "color": "#FF0000", "min": -20, "max": -15},
                {"level": 2, "color": "#FFFF00", "min": -15, "max": -10},
                {"level": 3, "color": "#008000", "min": -10, "max": -3},
            ],
        },
    ],
    "5G": [
        {
            "name": "rsrp",
            "signal_type": "quantity",
            "levels": [
                {"level": 1, "color": "#FF0000", "min": -140, "max": -120},
                {"level": 2, "color": "#FFA500", "min": -120, "max": -110},
                {"level": 3, "color": "#008000", "min": -110, "max": -80},
            ],
        },
        {
            "name": "rsrq",
            "signal_type": "quality",
            "levels": [
                {"level": 1, "color": "#FF0000", "min": -20, "max": -15},
                {"level": 2, "color": "#FFFF00", "min": -15, "max": -10},
                {"level": 3, "color": "#008000", "min": -10, "max": -3},
            ],
        },
    ],
}
