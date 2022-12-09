import argparse

import torch
import esm

import biotite.structure.io as bsio

print('loading models')
model = esm.pretrained.esmfold_v1()
model = model.eval().cuda()

# Optionally, uncomment to set a chunk size for axial attention. This can help reduce memory.
# Lower sizes will have lower memory requirements at the cost of increased speed.
# model.set_chunk_size(128)

# sequence = "MKTVRQERLKSIVRILERSKEPVSGAQLAEELSVSRQVIVQDIAYLRSLGYNIVATPRGYVLAGG"
# Multimer prediction can be done with chains separated by ':'

parser = argparse.ArgumentParser()
parser.add_argument("sequence", type=str, help="amino acid sequence to fold")
args = parser.parse_args()

print('infering sequence')
with torch.no_grad():
    output = model.infer_pdb(args.sequence)

print('saving pdb')
with open("outputs/result.pdb", "w") as f:
    f.write(output)

print('calc b factor')
struct = bsio.load_structure("outputs/result.pdb", extra_fields=["b_factor"])
print(struct.b_factor.mean())  # this will be the pLDDT