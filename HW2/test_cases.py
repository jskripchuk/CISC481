KB_1 = [
    [pred("grandparent", "?x", "?y"), pred("parent", "?x", "?z"), pred("parent", "?z", "?y")],
    [pred("parent", "Brian", "Doug")],
    [pred("parent", "Doug", "Mary")],
    [pred("parent", "Mary", "Sue")]
]

GOAL_1 = pred("grandparent", "?x1", "?y1")

KB_2 = [
    [pred("aunt","?x","?y"), pred("sister","?x","?z"), pred("mother","?z","?y")],
    [pred("aunt","?x","?y"), pred("sister","?x","?z"), pred("father","?z","?y")],
    [pred("sister","Mary","Sue")],
    [pred("sister","Mary","Doug")],
    [pred("father","Doug","John")],
    [pred("mother","Sue","Paul")]
]

GOAL_2 = pred("aunt","?x","?y")

KB_3 = [
    [pred("simple_sentence", "?x", "?y", "?z", "?u" ,"?v"),
     pred("noun_phrase", "?x", "?y"),
     pred("verb_phrase", "?z", "?u", "?v")],

    [pred("noun_phrase", "?x", "?y"), pred("article", "?x"), pred("noun", "?y")],
    [pred("verb_phrase","?x","?y","?z"), pred("verb","?x"), pred("noun_phrase","?y","?z")],
    [pred("article","a")],
    [pred("article","the")],
    [pred("noun","man")],
    [pred("noun","dog")],
    [pred("verb","likes")],
    [pred("verb","bites")]

    ]

GOAL_3 = pred("simple_sentence","?x","?y","?z","?u","?v")

KB_4 = [
    [pred("ancestor", "?x","?y"), pred("parent","?x","?y")],
    [pred("ancestor","?x","?y"), pred("ancestor","?x","?z"), pred("parent","?z","?y")],
    [pred("parent","Mary","Paul")],
    [pred("parent","Sue","Mary")]
]

GOAL_4 = pred("ancestor","?x","?y")

KB_5 = [
    [pred("ancestor","?x","?y"), pred("ancestor","?x","?z"), pred("parent","?z","?y")],
    [pred("ancestor", "?x","?y"), pred("parent","?x","?y")],
    [pred("parent","Mary","Paul")],
    [pred("parent","Sue","Mary")]
]

GOAL_5 = pred("ancestor","?x","?y")