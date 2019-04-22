# noinspection PyPackageRequirements
import wx

import gui.mainFrame
from gui.contextMenu import ContextMenu
from gui.itemStats import ItemStatsDialog
from service.fit import Fit
from service.settings import ContextMenuSettings


class ItemStats(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, mainItem, selection):
        return srcContext in ("marketItemGroup", "marketItemMisc",
                              "fittingModule", "fittingCharge",
                              "fittingShip", "baseShip",
                              "cargoItem", "droneItem",
                              "implantItem", "boosterItem",
                              "skillItem", "projectedModule",
                              "projectedDrone", "projectedCharge",
                              "itemStats", "fighterItem",
                              "implantItemChar", "projectedFighter",
                              "fittingMode")

    def getText(self, itmContext, mainItem, selection):
        return "{0} Stats".format(itmContext if itmContext is not None else "Item")

    def activate(self, fullContext, mainItem, selection, i):
        srcContext = fullContext[0]
        if srcContext == "fittingShip":
            fitID = self.mainFrame.getActiveFit()
            sFit = Fit.getInstance()
            stuff = sFit.getFit(fitID).ship
        elif srcContext == "fittingMode":
            stuff = selection[0].item
        else:
            stuff = selection[0]

        if srcContext == "fittingModule" and stuff.isEmpty:
            return

        mstate = wx.GetMouseState()
        reuse = False

        if mstate.shiftDown:
            reuse = True

        if self.mainFrame.GetActiveStatsWindow() is None and reuse:
            ItemStatsDialog(stuff, fullContext)

        elif reuse:
            lastWnd = self.mainFrame.GetActiveStatsWindow()
            pos = lastWnd.GetPosition()
            maximized = lastWnd.IsMaximized()
            if not maximized:
                size = lastWnd.GetSize()
            else:
                size = wx.DefaultSize
                pos = wx.DefaultPosition
            ItemStatsDialog(stuff, fullContext, pos, size, maximized)
            lastWnd.Close()

        else:
            ItemStatsDialog(stuff, fullContext)


ItemStats.register()
