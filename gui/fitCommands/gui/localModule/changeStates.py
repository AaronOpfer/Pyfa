import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.module.localChangeStates import CalcChangeLocalModuleStatesCommand
from gui.fitCommands.helpers import InternalCommandHistory, restoreRemovedDummies
from service.fit import Fit


class GuiChangeLocalModuleStatesCommand(wx.Command):

    def __init__(self, fitID, mainPosition, positions, click):
        wx.Command.__init__(self, True, 'Change Local Module States')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.mainPosition = mainPosition
        self.positions = positions
        self.click = click
        self.savedRemovedDummies = None

    def Do(self):
        cmd = CalcChangeLocalModuleStatesCommand(
            fitID=self.fitID,
            mainPosition=self.mainPosition,
            positions=self.positions,
            click=self.click)
        success = self.internalHistory.submit(cmd)
        sFit = Fit.getInstance()
        sFit.recalc(self.fitID)
        self.savedRemovedDummies = sFit.fill(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success

    def Undo(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        restoreRemovedDummies(fit, self.savedRemovedDummies)
        success = self.internalHistory.undoAll()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
