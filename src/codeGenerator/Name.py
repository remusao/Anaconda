
def visit(self, t):
    toPrint = t.id
    if toPrint == "True":
        toPrint = "true"
    elif toPrint == "False":
        toPrint = "false"

    self.output.write(toPrint)
