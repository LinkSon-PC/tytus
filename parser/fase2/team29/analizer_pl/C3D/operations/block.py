from analizer_pl.abstract.instruction import Instruction
from analizer_pl.abstract.expression import TYPE
from analizer_pl.statement.expressions import code
from analizer_pl.abstract.environment import Environment
from analizer_pl.reports.Nodo import Nodo

class Block(Instruction):
    def __init__(
        self, function, declaration, blocks, exception, label, row, column
    ) -> None:
        super().__init__(row, column)
        self.function = function
        self.declaration = declaration
        self.blocks = blocks
        self.exception = exception
        self.label = label

    def execute(self, environment):
        newEnv = Environment(environment)
        decl = ""
        bl = ""
        defFunc = self.function.execute(newEnv).value
        for d in self.declaration:
            decl += d.execute(newEnv).value
        for b in self.blocks:
            bl += b.execute(newEnv).value
        return code.C3D(defFunc + decl + bl + "\n", "block", self.row, self.column)

    def dot(self):
        new = Nodo("BLOCK")
        new.addNode(self.function.dot())

        dec = Nodo("DECLARATION")
        new.addNode(dec)
        for d in self.declaration:
            dec.addNode(d.dot())

        inst = Nodo("INSTRUCTIONS")
        new.addNode(inst)

        for b in self.blocks:
            inst.addNode(b.dot())
        return new