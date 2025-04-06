from openroad import Design,Tech
import odb 


tech = Tech()

tech.readLef("NangateOpenCellLibrary.tech.lef")
tech.readLef("NangateOpenCellLibrary.macro.mod.lef")

design = Design(tech)

design.readDef("jpeg.def")

design.writeDb("test.odb")

