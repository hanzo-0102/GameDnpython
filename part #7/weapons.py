class Weapon:
    def __init__(self, name, distance, manacost, damage, type):
        self.name = name
        self.dist = distance
        self.manacost = manacost
        self.damage = damage
        self.type = type


weapon_list = {
    'magicwand': Weapon('magicwand', 100, 2, 1, 'range'),
    'woodensword': Weapon('woodensword', 600, 0, 2, 'melee'),
    'golemgun': Weapon('golemgun', 100, 4, 8, 'range'),
    'bow': Weapon('bow', 100, 1, 3, 'range'),
    'crashedironsword': Weapon('crashedironsword', 600, 0, 3, 'melee'),
    'ironsword': Weapon('ironsword', 500, 0, 5, 'melee'),
    'ironspear': Weapon('ironspear', 300, 0, 3.5, 'melee'),
    'naturebow': Weapon('naturebow', 80, 0.5, 3.5, 'range')
}