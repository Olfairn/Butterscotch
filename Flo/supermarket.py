#%%

from PIL import Image
import numpy as np

im = Image.open('market.png')
market = np.array(im)
print(market.shape, market.dtype)

im2 = Image.open('tiles.png')
tiles = np.array(im2)
print(tiles.shape, tiles.dtype)
#%%
x = 4 * 32   # 5th column starting from 0
y = 1 * 32   # 2nd row
apple = tiles[y:y+32, x:x+32]
#%%
x = 10 * 32   # 5th column starting from 0
y = 5 * 32   # 2nd row
cross = tiles[y:y+32, x:x+32]
#%%
x = 11 * 32   # 5th column starting from 0
y = 1 * 32   # 2nd row
eggplant = tiles[y:y+32, x:x+32]

#%%
x = 4 * 32   # 5th column starting from 0
y = 2 * 32   # 2nd row
peach = tiles[y:y+32, x:x+32]
#%%
for x in range(7):
    tx = 1 * 32
    ty = x * 32
    market[ty:ty+32, tx:tx+32] = peach
    im = Image.fromarray(market)

im

#%%
im.save('supermarket_filled.png')

im