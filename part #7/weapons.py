class Weapon:
    def __init__(self, name, distance, manacost, damage):
        self.name = name
        self.dist = distance
        self.manacost = manacost
        self.damage = damage


weapon_list = {
    'magicwand': Weapon('magicwand', 100, 2, 1),
    'woodensword': Weapon('woodensword', 600, 0, 3),
    'golemgun': Weapon('golemgun', 100, 4, 8),
    'bow': Weapon('bow', 100, 3, 4)
}