from Processor import Processor
from TaskInput import TaskInput

FILE_NAME = '9-0.xls'

TASKS_INPUT_ARR = [
    TaskInput('Апрель', 0),
    TaskInput('Май', 1),
    TaskInput('Июнь', 2),
    TaskInput('Всё', [0, 1, 2]),
]

proc = Processor()
proc.load_df(FILE_NAME)
proc.calculate()
proc.print(TASKS_INPUT_ARR)
