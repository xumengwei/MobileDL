import json
import jsonpatch
import operator
import sys

DL_MODELS_JSON = sys.argv[1]
DL_MODELS_tmp_JSON = sys.argv[2]

result1 = ""
result2 = ""
with open(DL_MODELS_JSON) as f:
    # print(type(f))  # <class '_io.TextIOWrapper'>  也就是文本IO类型
    result1 = json.load(f)
    # print(result1)

with open(DL_MODELS_tmp_JSON) as f2:
    # print(f2)  # <class '_io.TextIOWrapper'>  也就是文本IO类型
    result2 = json.load(f2)

res = {}
item2 = result2.items()
# print(item2)
for key, value in item2:
    print(str(key))
    item2_sub = value.items()
    # print(value)
    res_sub = {}
    for key_sub,value_sub in item2_sub:
        # print(value_sub, result1[key][key_sub])
        # patch = jsonpatch.JsonPatch.from_diff(src, dst)
        if not operator.eq(value_sub, result1.get(key).get(key_sub)) and len(value_sub)>0:
            res_sub[key_sub] = value_sub
    res[key] = res_sub

print(res)

with open("./output/left.json", "w") as dump_f:
    json.dump(res, dump_f)