# shipProjectileDmgMC2
#
# Used by:
# Variations of ship: Rupture (3 of 3)
# Ship: Cynabal
# Ship: Moracha
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Cruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusMC2") * level)
