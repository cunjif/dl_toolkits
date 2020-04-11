''' Network architecture define 

like: 
    model = [
        (mode, (ksize, stride, padding, dilation))
        ...
    ]
'''

input_size = (413, 550)

which = None

model = [
    ('conv', (3, 4, 2, 1)),
    ('maxpool', (3, 2, 0, 1)),
    ('conv', (5, 1, 2, 1)),
    ('maxpool', (3, 2, 0, 1)),
    ('conv', (3, 1, 1, 1)),
    ('conv', (3, 1, 1, 1)),
    ('maxpool', (3, 2, 0, 1)),
]