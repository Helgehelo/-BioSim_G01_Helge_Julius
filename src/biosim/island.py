class Island:

    def __init__(self, island_map, ini_pop=None):
            self.map_list = []
            self.map_columns = len(island_map.splitlines()[0])
            self.map_rows = len(island_map.splitlines)
            map_dict = {"O": Ocean, "S": Savannah, "M": Mountain, "J": Jungle, "D": Desert}
            for line in island_map.splitlines():
                if len(line) != self.map_columns:
                    raise ValueError("Island map not rectangular")
                placeholder_list = []
                for nature_square_char in line:
                    try:
                        placeholder_list.append(map_dict[nature_square_char]()) # Creates nature objects
                    except KeyError:
                        raise ValueError
                map_list.append(placeholder_list)
            # Checks so that Ocean squares are on edges
            for nature_square in map_list[0]:
                if not isinstance(nature_square, Ocean):
                    raise ValueError
            for nature_square in map_list[len(map_list) - 1]:
                if not isinstance(nature_square, Ocean):
                    raise ValueError
            for nature_square in range(len(map_list)):
                if not isinstance(map_list[nature_square][0], Ocean):
                    raise ValueError
            for nature_square in range(len(map_list)):
                if not isinstance(map_list[nature_square][len(map_list[0]) - 1], Ocean):
                    raise ValueError


        if ini_pop:  # If an initial population is provided right away
            self.add_population(population=ini_pop)  # Call the add_population method

    def add_population(self, population):
        for square in population:
            square_location = square["loc"]
            row = square_location[0]
            column = square_location[1]
            if row <= 1 or row > self.map_rows:
                raise ValueError("Square dont exist")
            if column <= 1 or column > self.map_columns:
                raise ValueError("Square dont exist")
            nature_square = self.map_list[row-1][column-1]
            if not nature_square.habitable:
                raise ValueError("non habitable square provided")
            animal_pop = square["pop"]
            for animal in animal_pop:
                if animal["species"] == "Carnivore":
                    animal_object = Carn()
                    animal_object.a = animal["age"]
                    animal_object.w = animal["weight"]
                    animal_object.fitness_update()
                    nature_square.carn_list.append(animal_object)

                elif animal["species"] == "Herbivore":
                    animal_object = Herb()
                    animal_object.a = animal["age"]
                    animal_object.w = animal["weight"]
                    animal_object.fitness_update()
                    nature_square.herb_list.append(animal_object)
                else:
                    raise ValueError("Incorrect Species name in dict")

    def one_year(self):
        for row in self.map_list:
            for nature_square in row:
                if nature_square.habitable:
                    nature_square.fodder_update()
                    nature_square.feed_all_animals()
                    nature_square.birth_all_animals()
        self.migration()
        for row in self.map_list
            for nature_square in row:
                if nature_square.habitable:
                    nature_square.aging_all_animals()
                    nature_square.weightloss_all_animals()
                    nature_square.death_all_animals()

    def migration(self):
        for row in range(1, self.map_rows - 1):
            for column in range(1, self.map_columns - 1):
                nature_square = self.map_list[row][column]
                if nature_square.habitable:
                    north = self.map_list[row - 1][column]
                    east = self.map_list[row][column + 1]
                    south = self.map_list[row + 1][column]
                    west = self.map_list[row][column - 1]
                    neighbors = (north, east, south, west)
                    nature_square.migrate_all_animals(neighbors)


    def animals_on_square(self):
        """Makes a list with the number of herbivores and carnivores on every
        nature_square, indexing is adjusted so that square(0,0) becomes
        square(1,1), this is done because pandas.dataframe starts index from
        (1, 1)"""
        animal_count_list = []
        for i in range(self.map_rows):
            for j in range(self.map_columns):
                nature_square = self.map_list[i][j]
                animal_count_list.append([i+1, j+1, nature_square.herbivore_number(),
                                          nature_square.carnivore_number()])
        return animal_count_list

    def count_animals(self):
        """
        Count animals on the island.

        :return: tuple, three-element tuple with counts of Herbivores and Carnivores on the island
        and the sum of these.
        """
        animal_count_list = self.animals_on_square()
        herbivore_count = sum(row[2] for row in animal_count_list)
        carnivore_count = sum(row[3] for row in animal_count_list)
        animal_sum = herbivore_count + carnivore_count
        return herbivore_count, carnivore_count, animal_sum
