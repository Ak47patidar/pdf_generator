
from reportlab.platypus import Flowable
from reportlab.lib import colors

from Utils.utils import get_data
from FMO_Letter.components import Components


class MyLineFlowable(Flowable):
    def __init__(self, width, lWidth=2):
        Flowable.__init__(self)
        self.width = width
        self.line_width = lWidth

    def draw(self):
        self.canv.setLineWidth(self.line_width)
        self.canv.setStrokeColor(colors.black)
        self.canv.line(0, 0, self.width, 0)


if __name__ == '__main__':
    data= get_data('Resource\\input_multiple_policy_dummy')
    for each_policy in data:
        comp = Components(each_policy)
        comp.generate_entire_flow_components()
    
    # import json
    # # assuming you already have your dictionary in variable `data`
    # with open("data.json", "w", encoding="utf-8") as f:
    #     json.dump(data, f, indent=4, ensure_ascii=False)

    # print("✅ Data successfully saved to data.json")

    

