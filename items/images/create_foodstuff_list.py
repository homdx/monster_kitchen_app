import csv
import json

background_size = [1322, 884]

food = csv.reader(open('folder_monster.csv', 'rb'), delimiter=',')
food_dict = {'data': {}}
for stuff in food:
    print(stuff)
    if stuff[1] != 'name':
        pos = [int(stuff[2]), int(stuff[3])]
        size = [int(stuff[4]), int(stuff[5])]
        pos[0] -= size[0] / 2  # shift from middle to bottom-left
        pos[1] += size[1] / 2  # shift from middle to bottom-left

        food_dict['data'][stuff[1]] = {
            'pos': [float(pos[0]) / float(background_size[0]),
                    1.0 - float(pos[1]) / float(background_size[1])],
            'size': [float(size[0]) / float(background_size[0]),
                    float(size[1]) / float(background_size[1])],
            'attributes': [stuff[9], stuff[10], stuff[11]]
        }
print(food_dict)
json.dump(food_dict, open('../food.json', 'w'))