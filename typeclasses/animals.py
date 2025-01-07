from evennia.utils.funcparser import FuncParser
from evennia.utils.funcparser import funcparser_callable_an

from typeclasses.characters import Character, LivingMixin
from typeclasses.mounts import Mount
from utils.utils import iter_to_multiline

from django.utils.translation import gettext as _

from random import randint

parser = FuncParser({"an": funcparser_callable_an})

class Animal(Character, LivingMixin):
    '''
    This is a base class for Animals.

    It will generate a description on object creation, based
    on the trait_options property. It holds the characteristics
    that will be formatted on the generated description.

    This class should NOT be used directly!
    It should ALWAYS be a parent class!
    This class uses it's own typeclass path to define it's
    'animal_type' property:
        animals.Animal.animal_type = animal
        animals.Cat.animal_type = cat
        animals.NetherDrake.animal_type = netherdrake*
        (* not particurlarly recommended)

    This is then used by the generate_animal() method to
    generate and set the descriptions.

    How to use:
        Use this class as parent for any animal. It
        But for more complex descriptions you should
        make a new class that inherits from this one and overload
        a couple things:
        
            trait_options: to customize what characteristics said
            animal could have.

            generate_animal(): to customize how the description
            itself is generated, using the characteristics you set
            on trait_options.
    '''

    appearance_template =  """
{header}
{desc}{characters}{things}
{exits}
{footer}
    """

    @property
    def trait_options():
        return {
        'fur_color':['black','white','grey'],
        'fur_density':['thin','thick','wavy'],
        'fur_length':['black','white','grey'],
        }
    
    @property
    def appearance(self):
        return self.db.appearance

    @property
    def animal_type(self):
        return self.typeclass_path.split('.')[-1].lower()

    def at_object_creation(self):
        # animal_type = self.typeclass_path.split('.')[-1].lower()
        super().at_object_creation()

        self.db.named = False
        if self.key != self.animal_type:
            self.db.named = True

        self.generate_animal()

    def get_display_name(self, looker=None, **kwargs):
        '''
        return object's name, if kwarg are used,
        checks what format it should be.
        '''
        display_name = f"|h{self.key}|H"
        if self.db.named:
            display_name = f"|h{self.key.capitalize()}|H"

        if not self.db.named:
            full_color_name = parser.parse(f"$an({self.appearance['color']})")# if 'wrinkle' not in self.appearance else 'a naked'
            article, color_name = full_color_name.split(' ', 1)
            display_name = f"{article} {color_name} |h{self.key}|H"
        else:
            self.appearance_template =  """
|B{name}|n
{header}
{desc}{characters}{things}
{exits}
{footer}
            """
            display_name += " the {animal}".format(animal = self.animal_type)

        if looker:
            # Check for Builder permission. If valid, display dbref (#XYZ)
            if looker.locks.check_lockstring(looker, "_dummy:perm(Builder)"):
                display_name +=  f"({self.dbref})"

        return display_name
    
    # def get_display_desc(self, looker, **kwargs):
    #     desc = self.db.desc, self.db.desc_appearance
    #     return iter_to_multiline(desc)
    
    # def move_around(self):
    #     print(f'{self.key} is moving!')

    def generate_animal(self):
        full_animal_type = parser.parse(f"$an({self.animal_type})").capitalize()

        trait_options = self.trait_options
        traits = {}
        
        for trait in trait_options:
            rand_index = randint(0, len(trait_options[trait])-1)
            traits[trait] = (trait_options[trait][rand_index])
        
        animal_description = (
            "{animal} with {color} fur, {density} and {length}."
            .format(animal=full_animal_type, color=traits['fur_color'], density=traits['fur_density'], length=traits['fur_length']) 
                    if traits['fur_length'] != 'medium'
                    else ("{animal} with {color}, {density} fur."
                     .format(animal=full_animal_type, color=traits['fur_color'], density=traits['fur_density'])
                     )
            )

        self.db.appearance = {
            'color':traits['fur_color'],
            'density':traits['fur_density'],
            'length':traits['fur_length'],
            }
            
        if traits['fur_pattern'] != 'plain':
            secondary_color = trait_options['fur_color'][randint(0,len(trait_options[trait])-1)]

            if secondary_color == traits['fur_color']:
                while secondary_color == traits['fur_color']:
                    secondary_color = trait_options['fur_color'][randint(0,len(trait_options[trait])-1)]

            animal_description = (
                "{animal} with {color1} and {color2} fur, {density} and {length} in a {pattern} pattern."
                .format(animal=full_animal_type, color1=traits['fur_color'], color2=secondary_color,
                        density=traits['fur_density'], pattern=traits['fur_pattern'],
                        length=traits['fur_length'])
                if traits['fur_length'] != 'medium'
                else "{animal} with {color1} and {color2} fur, {density} and in a {pattern} pattern."
                .format(animal=full_animal_type, color1=traits['fur_color'], color2=secondary_color,
                        density=traits['fur_density'], pattern=traits['fur_pattern'])
                )
            
            self.db.appearance = {
                'color':traits['fur_color'],
                'density':traits['fur_density'],
                'length':traits['fur_length'],
                'pattern':traits['fur_pattern'],
                }

        self.db.desc = animal_description

class Cat(Animal):
    '''
    Cats!
    Procedural cats!
    '''
    _content_types = ("animal",)

    trait_options = {
        'fur_color':['black','white','grey','auburn','silver','dark grey','orange','brown'],
        'fur_density':['feathery','fuzzy','thick','thin','straight'], #'naked'],
        'fur_pattern':['striped','spotted','plain'],
        # 'fur_length':['naked','short','long'],
        'fur_length':['short','medium','long'],
        'skin_color':['beige','black','grey'],
        'skin_wrinkle':['smooth','wrinkly'],
        }

    # def at_object_creation(self):       
    #     trait_options = self.trait_options
    #     traits = {}

    #     if not trait_options:
    #         return super().at_object_creation()
        
    #     for trait in trait_options:
    #         rand_index = randint(0, len(trait_options[trait])-1)
    #         traits[trait] = (trait_options[trait][rand_index])
        
    #     cat_description = (
    #         "A cat with {color} fur, {density} and {length}."
    #         .format(color=traits['fur_color'], density=traits['fur_density'], pattern=traits['fur_pattern'], length=traits['fur_length'])
    #         )

    #     self.db.appearance = {
    #         'color':traits['fur_color'],
    #         'density':traits['fur_density'],
    #         'pattern':traits['fur_pattern'],
    #         }

    #     # THINKING ABOUT NOT EVEN HAVING NAKED CATS
    #     if 'naked' in traits['fur_length']:
    #         cat_description = (
    #             "A naked cat with {wrinkle} {color} skin."
    #             .format(color=traits['skin_color'], wrinkle=traits['skin_wrinkle'])
    #             )
        
    #         self.db.appearance = {
    #             'color':traits['skin_color'],
    #             'wrinkle':traits['skin_wrinkle'],
    #             }
            
    #     if ('spotted' in traits['fur_pattern']) or ('striped' in traits['fur_pattern']):
    #         secondary_color = trait_options['fur_color'][randint(0,len(trait_options[trait])-1)]

    #         if secondary_color == traits['fur_color']:
    #             while secondary_color == traits['fur_color']:
    #                 secondary_color = trait_options['fur_color'][randint(0,len(trait_options[trait])-1)]

    #         cat_description = (
    #             "A cat with {color1} and {color2} fur, {density} and {length} in a {pattern} pattern."
    #             .format(color1=traits['fur_color'], color2=secondary_color, density=traits['fur_density'], pattern=traits['fur_pattern'], length=traits['fur_length'])
    #             )

    #         self.db.appearance = {
    #             'color':traits['fur_color'],
    #             'color2':secondary_color,
    #             'density':traits['fur_density'],
    #             'pattern':traits['fur_pattern'],
    #             }

            
    #     super().at_object_creation()
    #     self.db.desc = cat_description        
    #     return

class Dog(Animal):
    '''
    Dogs! Man's best friend.
    '''
    _content_types = ("animal",)

    trait_options = {
        'fur_color':['black','white','grey','auburn','silver','dark grey','orange','brown'],
        'fur_density':['feathery','fuzzy','thick','thin','straight'],
        'fur_pattern':['spotted','plain'],
        'fur_length':['short','medium','long'],
        'skin_color':['beige','black','grey'],
        }

    
class Horse(Animal, Mount):
    '''
    The standard mount in the Doomland.
    '''
    _content_types = ("mount",)
    
    trait_options = {
        'fur_color':['black','white','grey','auburn','dark grey','brown'],
        'fur_density':['feathery','fuzzy','thick','thin','straight'],
        'fur_pattern':['spotted','plain'],
        'mane_style':['straight', 'braided', 'fuzzy', 'scraggly', 'wavy'],
        'mane_length':['short','medium','long'],
        'skin_color':['beige','black','grey'],
        }
        
    def generate_animal(self):
            full_animal_type = parser.parse(f"$an({self.animal_type})").capitalize()

            trait_options = self.trait_options
            traits = {}
        
            for trait in trait_options:
                rand_index = randint(0, len(trait_options[trait])-1)
                traits[trait] = (trait_options[trait][rand_index])
        
            animal_description = (
                "{animal} with {color} and {density} fur, with a {style} {length} mane."
                .format(animal=full_animal_type, color=traits['fur_color'], density=traits['fur_density'], length=traits['mane_length'], style=traits['mane_style']) 
                )

            self.db.appearance = {
                'color':traits['fur_color'],
                'density':traits['fur_density'],
                'style':traits['mane_style'],
                'length':traits['mane_length'],
                }
            
            if traits['fur_pattern'] != 'plain':
                secondary_color = trait_options['fur_color'][randint(0,len(trait_options[trait])-1)]

                if secondary_color == traits['fur_color']:
                    while secondary_color == traits['fur_color']:
                        secondary_color = trait_options['fur_color'][randint(0,len(trait_options[trait])-1)]

                animal_description = (
                    "{animal} with {density} fur, {color1} and {color2} in a {pattern} pattern with a {style}, {length} mane."
                    .format(animal=full_animal_type, color1=traits['fur_color'], color2=secondary_color,
                            density=traits['fur_density'], pattern=traits['fur_pattern'],
                            length=traits['mane_length'], style=traits['mane_style'])
                    )
            
                self.db.appearance = {
                    'color':traits['fur_color'],
                    'density':traits['fur_density'],
                    'pattern':traits['fur_pattern'],
                    'length':traits['mane_length'],
                    'style':traits['mane_style'],
                    }

            self.db.desc = animal_description
            
