
__version__ = "1.0.0v"

RES = 800, 600
DEFULT_WIDTH, DEFULT_HIGTH = RES
ALPA = "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM +×÷=/_±≈≠≡€£¥₩!@#$%^&*()-‐—\'\"№٪‰:;,?‽`~\\|<>\{\}\[\]¡¿.°•○●□■♤♡◇♧☆▪︎¤《》【〔「『】〕」』♠︎♥︎◆♣︎★😂🤣😅😆😁😄😃😀🤩😍🥰😇😊😉🙃🙂😛😋🥲😙😚☺😗😘🤔🤫🤭🤗🤑😝🤪😜🙄😒😏😶😑😐🤨🤐😷😴🤤😪😔😌🤥😬🥴🥶🥵🤧🤮🤢🤕🤒🧐🤓😎🥸🥳🤠🤯😵😳😲😯😮☹🙁😟😕😭😢😥😰😨😧😦🥺🥱😫😩😓😞😣😖😱🤬😠😡😤👋🤚🖐✋🖖👌🤌🤏✌🤞🤟🤘🤙👈👉👆🖕👇☝👍👎✊👊🤛🤜👏🙌👐🤲🤝🙏🌍🧱🪟🏠🧨💧🔥⚡❄☄🏡🕌🛕🕍🕋⭐🌟🧨🎈⚽️⚾️🥎🏀🏐🏈🏉🔴🟠🟡🟢🔵🟣🟤⚪⚫🟥🟧🟨🟩🟦🟪🟫⬛⬜🔘◼◻◽▪️▫️🔶️🔷️🔹️🔸️🔹️🔺️🔻💠🔲🔳"
KEYS = [ch for ch in ALPA]
CELLS = {k : KEYS[k] for k in range(342)}
_CELLS = {v : k for k, v in CELLS.items()}
CODE = '\n'

@staticmethod
def convert_to_bool(value): return True if value else False
@staticmethod
def remote(clist=None, **kwargs):
    result = []
    chart, graph, shape = kwargs.get('chart', False), kwargs.get('graph', False), kwargs.get('shape', False)
    if chart: data = _CELLS
    if graph or shape: data = CELLS
    for i in clist:
        if chart or graph: scape = []
        if shape: scape = ''
        for j in i:
            struc = f'{j}' if shape else [data[j]]
            scape = scape.__add__(struc)
        result.append(scape) 
    return result
@staticmethod
def remove_char(string, del_char, pops):
    update_str = []
    nopops = 0
    for char in string:
        if char == del_char and nopops < pops: nopops += 1
        else: update_str.append(char)
    return ''.join(update_str)