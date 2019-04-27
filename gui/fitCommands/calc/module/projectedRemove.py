import wx
from logbook import Logger

import eos.db
from service.fit import Fit
from gui.fitCommands.helpers import ModuleInfo


pyfalog = Logger(__name__)


class CalcRemoveProjectedModuleCommand(wx.Command):

    def __init__(self, fitID, position, commit=True):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.position = position
        self.commit = commit
        self.savedModInfo = None

    def Do(self):
        pyfalog.debug('Doing removal of projected module from position {} on fit {}'.format(self.position, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        mod = fit.projectedModules[self.position]
        self.savedModInfo = ModuleInfo.fromModule(mod)
        del fit.projectedModules[self.position]
        if self.commit:
            eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing removal of projected module {} on fit {}'.format(self.savedModInfo, self.fitID))
        from .projectedAdd import CalcAddProjectedModuleCommand
        cmd = CalcAddProjectedModuleCommand(
            fitID=self.fitID,
            modInfo=self.savedModInfo,
            position=self.position,
            commit=self.commit)
        return cmd.Do()
