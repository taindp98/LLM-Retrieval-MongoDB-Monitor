visual_language_generation = """
    You possess in-depth knowledge of natural images and can describe them with ease. \
    From the given input text indicating the category name of a certain object, your task involves the following steps:
    1-Imagine a scene containing the input object.
    2-Generate 4 descriptions about different key appearance features of the input object from the imagined scene, with each description having a maximum of 16 words.
    3-Output a JSON object containing the following key:
        "description": <list of 4 descriptions>

    Use the following examples:
        Input text: "sea lion"
        Answer: "description": ["A round-bellied seal sits on a rock, looking intently at something off-camera.", "The seal lies with flippers tucked, sleek body well-maintained.", "The seal's thick, smooth fur and large dark eyes show alertness and curiosity.", "Turquoise water contrasts with the seal's brown fur and grey rock, highlighting its natural environment."]
"""
