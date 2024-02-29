# local lib
from utils.json_ import jsonYOLO, Converter
from utils.segment import Predict
from utils.tile import tile_img
from utils.raster_metadata import meta

# global lib
import os
import cv2
import time
import numpy as np

from tqdm.auto import tqdm
from glob import glob

start = time.time()

# INPUT ADA DISINI --EDIT DI SINI SINI AJA--

# best model pakai runs/segment/train53/weights/best.pt
MODEL = 'best-10000.pt'
# image path
IMG = 'datasets/img/GORONTALO UTARA_50.tif'
# konstanta mengatur overlap || nilai overlap = 1 - nilai yang di input
OVER = 0.75
# mengatur tipe output || masks atau boxes
TIPE = 'masks'




# BAGIAN PROSESING --JANGAN DIEDIT--

# tile data image 
img, _ = tile_img(IMG).patchData(patch_dim=320, step_size=OVER)
print(f'shape tile dataset : {img.shape}')

# write tile data temporary
for i in range(img.shape[0]):
    cv2.imwrite(f'public/patch-temp/patch{i+1001}.png', img[i])

# Line dibawah untuk batch predict
LIST_IMG = glob('public/patch-temp/patch*.png')
with tqdm(total=len(LIST_IMG), desc='Proses deteksi bangunan', leave=True) as pbar:
    for i in LIST_IMG:
        a = Predict(img=i, model=MODEL).to_json(i.replace('png','json'), TIPE)
        pbar.update(1)

# Line untuk combine json
print('combine seluruh hasil prediction ...')
Predict.combine_json(OVER, TIPE)

# Convert json ke geojson
inp = 'public/patch-temp/combined_file.json'
out = 'public/patch-temp/gorontalo2.geojson'
# extent format --> [Xmin, Ymin, Xmax, Ymax]

ext = meta(IMG).cari_extent()
epsg = meta(IMG).get_epsg_from_raster()

Converter(inp, out, epsg=epsg, extent=ext, dim=_).to_geojson()

end = time.time()
mnt = (end - start)//60
dtk = np.ceil((end - start)- (mnt * 60))
print(f'Output berhasil di simpan di {out}')
print(f'--Alhamdulillah selesai dalam {mnt} menit {dtk} detik--')

# # Line dibawah untuk plot polygon dari json
# out_json = jsonYOLO(path='public/patch-temp/combined_file.json').load()
# jsonYOLO.plot_polygons(out_json, image_shape=(_.dim[0],_.dim[1]))
