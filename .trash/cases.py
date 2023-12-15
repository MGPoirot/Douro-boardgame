"""
You can add case sets which can be called using
> python test.py --cases your_case_name
"""

example = {"schwierigkeit-sehrleicht_size-10_pins-4_kanten-13": [(0, 1), (4, 4), (8, 3), (2, 5)],
            "schwierigkeit-mittel_size-10_pins-7_kanten-22": [(3, 5), (3, 10), (5, 5), (5, 7), (7, 2), (10, 2), (10, 8), ]}

test = {
    "schwierigkeit-extremschwer_size-10_pins-12_kanten-29": [(1, 2), (1, 5), (2, 7), (3, 4), (4, 2), (5, 6), (6, 3), (6, 10),
                                                     (8, 6), (8, 8), (10, 5), (10, 8), ],
    "schwierigkeit-extremschwer_size-10_pins-12_kanten-30": [(1, 5), (1, 9), (2, 2), (4, 6), (5, 3), (5, 8), (7, 6), (7, 10),
                                                     (8, 3), (8, 7), (9, 5), (10, 6), ],
    "schwierigkeit-extremschwer_size-10_pins-12_kanten-32": [(1, 4), (2, 10), (3, 7), (4, 2), (6, 5), (6, 10), (7, 1), (7, 6),
                                                     (8, 5), (8, 9), (10, 6), (10, 8), ],
    "schwierigkeit-extremschwer_size-10_pins-12_kanten-33": [(1, 4), (1, 10), (2, 2), (3, 5), (4, 3), (4, 6), (6, 7), (6, 9),
                                                     (7, 1), (8, 7), (9, 4), (10, 9), ],
    "schwierigkeit-leicht_size-10_pins-6_kanten-23": [(2, 3), (2, 8), (6, 1), (6, 7), (10, 3), (10, 8), ],
    "schwierigkeit-leicht_size-10_pins-6_kanten-24": [(1, 5), (1, 10), (5, 2), (5, 10), (8, 1), (9, 6), ],
    "schwierigkeit-leicht_size-10_pins-6_kanten-24_version-2": [(2, 3), (2, 8), (6, 2), (6, 7), (10, 3), (10, 10), ],
    "schwierigkeit-leicht_size-10_pins-6_kanten-25": [(1, 2), (1, 6), (5, 10), (6, 2), (10, 6), (10, 10), ],
    "schwierigkeit-leicht_size-10_pins-6_kanten-25_version-2": [(2, 2), (2, 7), (6, 3), (6, 7), (10, 1), (10, 10), ],
    "schwierigkeit-mittel_size-10_pins-7_kanten-22": [(3, 5), (3, 10), (5, 5), (5, 7), (7, 2), (10, 2), (10, 8), ],
    "schwierigkeit-mittel_size-10_pins-7_kanten-24": [(2, 10), (3, 6), (7, 2), (7, 4), (9, 4), (10, 2), (10, 10), ],
    "schwierigkeit-mittel_size-10_pins-7_kanten-25": [(1, 1), (1, 6), (4, 8), (6, 2), (7, 8), (10, 3), (10, 6), ],
    "schwierigkeit-mittel_size-10_pins-7_kanten-26": [(1, 8), (2, 2), (4, 5), (5, 1), (7, 6), (8, 3), (10, 10), ],
    "schwierigkeit-mittel_size-10_pins-7_kanten-27": [(1, 5), (2, 10), (3, 9), (4, 2), (7, 6), (8, 1), (10, 10), ],
    "schwierigkeit-sehrleicht_size-10_pins-5_kanten-24": [(1, 2), (1, 10), (8, 3), (9, 10), (10, 3), ],
    "schwierigkeit-sehrleicht_size-10_pins-5_kanten-24_version-3": [(1, 3), (2, 10), (9, 2), (10, 3), (10, 10), ],
    "schwierigkeit-sehrleicht_size-10_pins-5_kanten-24_version-4": [(1, 2), (1, 9), (8, 10), (9, 2), (10, 9), ],
    "schwierigkeit-sehrleicht_size-10_pins-5_kanten-25": [(1, 2), (1, 9), (8, 9), (9, 10), (10, 1), ],
    "schwierigkeit-sehrleicht_size-10_pins-5_kanten-25_version-2": [(1, 9), (2, 1), (2, 10), (9, 2), (10, 10), ],
    "schwierigkeit-sehrschwer_size-10_pins-9_kanten-27": [(1, 8), (1, 10), (3, 4), (4, 10), (6, 2), (8, 2), (8, 6), (10, 4),
                                                  (10, 8), ],
    "schwierigkeit-sehrschwer_size-10_pins-9_kanten-27_version-2": [(1, 2), (1, 8), (2, 10), (4, 4), (4, 6), (6, 2), (6, 6),
                                                            (7, 4), (9, 10), ],
    "schwierigkeit-sehrschwer_size-10_pins-9_kanten-28": [(1, 4), (1, 10), (3, 2), (5, 6), (5, 8), (7, 6), (7, 9), (9, 2),
                                                  (9, 8), ],
    "schwierigkeit-sehrschwer_size-10_pins-9_kanten-29": [(2, 3), (2, 8), (4, 10), (6, 4), (6, 6), (8, 1), (8, 6), (10, 4),
                                                  (10, 10), ],
    "schwierigkeit-sehrschwer_size-10_pins-9_kanten-29_version-2": [(1, 3), (1, 9), (4, 2), (5, 6), (6, 7), (7, 10), (8, 6),
                                                            (9, 8), (10, 2), ],
    "schwierigkeit-schwer_size-10_pins-8_kanten-26": [(1, 3), (1, 10), (6, 2), (6, 8), (8, 6), (8, 9), (10, 6), (10, 8), ],
    "schwierigkeit-schwer_size-10_pins-8_kanten-28": [(1, 7), (2, 2), (4, 10), (6, 6), (7, 2), (7, 10), (10, 3), (10, 7), ],
    "schwierigkeit-schwer_size-10_pins-8_kanten-28_version-2": [(1, 6), (1, 10), (2, 3), (4, 7), (5, 2), (5, 10), (9, 4),
                                                        (10, 9), ],
    "schwierigkeit-schwer_size-10_pins-8_kanten-30": [(1, 4), (1, 10), (3, 1), (3, 6), (7, 2), (7, 7), (10, 4), (10, 10), ],
    "schwierigkeit-schwer_size-10_pins-8_kanten-31": [(1, 3), (1, 10), (2, 6), (4, 1), (5, 5), (7, 10), (10, 2), (10, 8), ]}

extreme = {"name-Rubens_schwierigkeit-extremschwer_size-7_pins-15_kanten-29": [(0, 4), (0, 7), (1, 5), (2, 1), (2, 3), (3, 0), (3, 7), (4, 2), (4, 4), (4, 6), (5, 0), (5, 5), (6, 4), (7, 2), (7, 7)]}
